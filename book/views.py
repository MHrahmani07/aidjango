# book/views.py

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
import random
import datetime
from django.utils import timezone
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth import authenticate 
from .models import Book, VerificationCode
from .forms import BookForm, CodeVerificationForm, CustomUserCreationForm
from django.contrib.auth.models import User
from django.db.models import Count # For random ordering
import random # For truly random selection
from django.http import JsonResponse, HttpResponse




def home_view(request):
    return render(request, 'home.html')

# Book Views
class BookListView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Book.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category', '')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_favorited'] = self.object.favorited_by.filter(id=self.request.user.id).exists()
        else:
            context['is_favorited'] = False
        return context

class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_form.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.is_staff

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_form.html'
    context_object_name = 'book'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.is_staff

class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'book/book_confirm_delete.html'
    context_object_name = 'book'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        return self.request.user.is_staff

# Authentication Views
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        VerificationCode.objects.filter(user=user).delete()

        verification_code_str = str(random.randint(100000, 999999))
        expires_at = timezone.now() + datetime.timedelta(minutes=15)

        VerificationCode.objects.create(
            user=user,
            code=verification_code_str,
            expires_at=expires_at
        )

        mail_subject = 'Verify your My Bookstore account'
        message = render_to_string('registration/email/verification_code_email.html', {
            'user': user,
            'verification_code': verification_code_str,
            'site_name': 'My Bookstore',
            'code_lifespan_minutes': 15,
        })
        to_email = user.email

        email = EmailMessage(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])
        email.send()

        messages.success(self.request, 'An activation code has been sent to your email. Please check your inbox (and spam folder).')
        return redirect('verify_code_entry')

@login_required
def profile_view(request):
    favorited_books = request.user.favorite_books.all()
    return render(request, 'registration/profile.html', {
        'user': request.user,
        'favorited_books': favorited_books
    })

@login_required
def toggle_favorite_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user = request.user

    if request.method == 'POST':
        if book.favorited_by.filter(id=user.id).exists():
            book.favorited_by.remove(user)
        else:
            book.favorited_by.add(user)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse_lazy('book_detail', kwargs={'pk': pk})))



def verify_code_view(request):
    """
    Allows user to enter verification code sent to their email.
    """
    if request.user.is_authenticated and request.user.is_active:
        messages.info(request, 'Your account is already activated.')
        return redirect('profile')

    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['code']
            
            try:
                
                verification_entry = VerificationCode.objects.filter(
                    code=entered_code,
                    user__is_active=False,
                    expires_at__gt=timezone.now()
                ).order_by('-created_at').first()

                if verification_entry:
                    user_to_activate = verification_entry.user
                    user_to_activate.is_active = True
                    user_to_activate.save()
                    verification_entry.delete()

                    messages.success(request, 'Your account has been successfully activated! You can now log in.')
                    return redirect('login')
                else:
                    messages.error(request, 'Invalid or expired verification code. Please try again or sign up.')
            except VerificationCode.DoesNotExist:
                messages.error(request, 'Invalid verification code. Please try again.')
            except Exception as e:
                messages.error(request, f'An unexpected error occurred during verification: {e}')
                
    else:
        form = CodeVerificationForm()

    return render(request, 'registration/verify_code_entry.html', {'form': form})



class CustomLoginView(DjangoLoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm

    def post(self, request, *args, **kwargs):
        """
        Overrides the POST method to add an explicit check for inactive users.
        """
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if not user.is_active:
                   
                    messages.warning(request, 'Your account is not active. Please verify your email to log in.')
                    return redirect('verify_code_entry')
                else:
                    
                    return self.form_valid(form) 
            else:
                
                messages.error(request, 'Invalid username or password. Please try again.')
                return self.form_invalid(form) 
        else:
            return self.form_invalid(form)
    pass

# book/views.py
# ... (imports) ...


def get_random_book_api(request):
    if request.method == 'GET':
        books_count = Book.objects.count()
        if books_count == 0:
            return JsonResponse({'status': 'error', 'message': 'No books available'}, status=404)

        # Get a random book
        random_index = random.randint(0, books_count - 1)
        random_book = Book.objects.all()[random_index]

        data = {
            'id': random_book.id,
            'name': random_book.name,
            'publisher': random_book.publisher,
            'provider': random_book.provider,
            'price': str(random_book.price), # Convert Decimal to string
            'category': random_book.category,
            'category_display': random_book.get_category_display(),
            # Add image/pdf URLs if needed by LLM
            'image_url': request.build_absolute_uri(random_book.book_image.url) if random_book.book_image else None,
            'pdf_url': request.build_absolute_uri(random_book.book_pdf.url) if random_book.book_pdf else None,
        }
        return JsonResponse({'status': 'success', 'book': data})
    return JsonResponse({'status': 'error', 'message': 'Only GET requests allowed'}, status=405)