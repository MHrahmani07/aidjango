

from django.db import models
from django.contrib.auth.models import User 
from book.models import Book # 

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts')
    
    related_book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, related_name='blog_posts')
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date'] 

    def __str__(self):
        return self.title
