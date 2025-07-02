# book/forms.py
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm # Import Django's default UserCreationForm
from .models import Book, VerificationCode

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'publisher', 'provider', 'price', 'category', 'book_pdf', 'book_image']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'publisher': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'provider': forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'price': forms.NumberInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'category': forms.Select(attrs={'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50'}),
            'book_pdf': forms.FileInput(attrs={'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),
            'book_image': forms.FileInput(attrs={'class': 'mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'}),
        }

class CodeVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50 text-center text-xl font-mono tracking-widest',
            'placeholder': 'Enter 6-digit code',
            'inputmode': 'numeric',
            'pattern': '[0-9]{6}',
        }),
        help_text="Please enter the 6-digit code sent to your email address."
    )

# New: Custom User Creation Form to include email
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, # Make email a required field
        widget=forms.TextInput(attrs={
            'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50',
            'placeholder': 'your.email@example.com'
        })
    )

    class Meta(UserCreationForm.Meta): # Inherit Meta from UserCreationForm
        model = User # Explicitly use Django's User model
        fields = UserCreationForm.Meta.fields + ('email',) # Add 'email' to the default fields
