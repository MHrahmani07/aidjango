# blog/urls.py

from django.urls import path
# Import the new generation view
from .views import BlogPostListView, BlogPostDetailView, generate_and_add_blog_post

urlpatterns = [
    # URL for listing all blog posts
    path('', BlogPostListView.as_view(), name='blog_list'),
    
    
    path('<int:pk>/', BlogPostDetailView.as_view(), name='blog_detail'),
    path('generate-new-post/', generate_and_add_blog_post, name='generate_new_blog_post'),
]
