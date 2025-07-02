# book/models.py

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('persian', 'Persian books'),
        ('computer', 'National computer book'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    publisher = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
    )
    favorited_by = models.ManyToManyField(User, related_name='favorite_books', blank=True)
    book_pdf = models.FileField(upload_to='books/pdfs/', blank=True, null=True) # Paths within MEDIA_ROOT are fine
    book_image = models.ImageField(upload_to='books/images/', blank=True, null=True) # Paths within MEDIA_ROOT are fine

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class VerificationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField() 

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Code for {self.user.username}: {self.code}"
