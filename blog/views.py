# blog/views.py

from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from book.models import Book # Import Book model
from .models import BlogPost
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy # For redirects
from django.contrib.auth.decorators import login_required, user_passes_test # For staff check
import requests # For making HTTP requests to OpenAI
import json # For handling JSON data
import random # For picking a random book
from django.conf import settings # To access OPENAI_API_KEY


# Blog Post List View
class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blog_posts'
    paginate_by = 5

# Blog Post Detail View
class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

# New: View to generate and add a blog post from OpenAI
@login_required # Only logged-in users can trigger this
@user_passes_test(lambda u: u.is_staff) # Only staff users (admins) can trigger this
def generate_and_add_blog_post(request):
    if request.method == 'POST':
        # 1. Fetch a random book
        books_count = Book.objects.count()
        if books_count == 0:
            messages.error(request, "No books available to generate a blog post about.")
            return redirect('blog_list')

        # Get a random book from the database
        random_index = random.randint(0, books_count - 1)
        random_book = Book.objects.all()[random_index]

        # 2. Prepare the prompt for OpenAI
        # We'll ask for JSON output for easier parsing
        prompt_messages = [
            {"role": "system", "content": "You are a helpful assistant specialized in writing engaging blog posts about books. Provide the response strictly in JSON format with 'title' and 'content' keys. The content should be a well-formatted blog post, using paragraphs and potentially markdown for headings."},
            {"role": "user", "content": f"Write a compelling blog post of 300-500 words about the book titled '{random_book.name}' by publisher '{random_book.publisher}', which is a '{random_book.get_category_display()}' book. Highlight its unique aspects and encourage readers to explore it. Also, provide a catchy title for the blog post."}
        ]

        openai_api_key = settings.OPENAI_API_KEY
        if not openai_api_key:
            messages.error(request, "OpenAI API key is not configured in settings.")
            return redirect('blog_list')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }
        payload = {
            "model": "gpt-3.5-turbo", # You can try "gpt-4" if you have access
            "messages": prompt_messages,
            "max_tokens": 1500, # Adjust based on desired content length
            "temperature": 0.7,
            "response_format": {"type": "json_object"} # Crucial for JSON output
        }

        try:
            # 3. Make API call to OpenAI
            openai_response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            openai_response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            response_data = openai_response.json()

            # Extract title and content from OpenAI's JSON response
            generated_content_str = response_data['choices'][0]['message']['content']
            
            # OpenAI now reliably returns JSON string if response_format is set.
            # Parse the content string as JSON.
            generated_blog_data = json.loads(generated_content_str)
            blog_title = generated_blog_data.get('title', 'Generated Blog Post')
            blog_content = generated_blog_data.get('content', 'No content generated.')

            # 4. Save the new BlogPost
            # Assign the currently logged-in staff user as the author
            author_user = request.user 
            BlogPost.objects.create(
                title=blog_title,
                content=blog_content,
                author=author_user,
                related_book=random_book
            )
            messages.success(request, f"Successfully generated and added a blog post: '{blog_title}'")
            
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Failed to connect to OpenAI API: {e}")
        except json.JSONDecodeError:
            messages.error(request, "Failed to parse JSON response from OpenAI. Check API key or response format.")
        except KeyError:
            messages.error(request, "Unexpected response format from OpenAI API. Could not extract title/content.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

    return redirect('blog_list') # Always redirect back to the blog list
