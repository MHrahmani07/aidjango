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
    book_pdf = models.FileField(upload_to='books/pdfs/', blank=True, null=True)
    book_image = models.ImageField(upload_to='books/images/', blank=True, null=True)

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

# New: Cart Model
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # A single user will have one cart. If user is deleted, their cart is deleted too.
    # For anonymous carts, you'd use a session key, but we'll keep it simple for now.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username if self.user else 'Anonymous'}"
    
    def get_total_price(self):
        return sum(item.get_total_item_price() for item in self.cartitem_set.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.cartitem_set.all())


# New: CartItem Model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        # Ensures that a specific book can only appear once in a given cart
        unique_together = ('cart', 'book')

    def __str__(self):
        return f"{self.quantity} x {self.book.name} in {self.cart.user.username}'s Cart"

    def get_total_item_price(self):
        return self.quantity * self.book.price
