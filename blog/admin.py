# blog/admin.py
from django.contrib import admin
from .models import BlogPost

admin.site.register(BlogPost)