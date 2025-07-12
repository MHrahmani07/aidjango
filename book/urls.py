# book/urls.py

from django.urls import path
from .views import (
    BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, 
    toggle_favorite_view, add_to_cart_view, 
    cart_detail_view, update_cart_item_quantity_view, remove_from_cart_view # Import new views
)

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('new/', BookCreateView.as_view(), name='book_create'),
    path('<int:pk>/edit/', BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('<int:pk>/toggle_favorite/', toggle_favorite_view, name='toggle_favorite'),
    path('<int:pk>/add_to_cart/', add_to_cart_view, name='add_to_cart'),

    # New: Cart URLs
    path('cart/', cart_detail_view, name='cart_detail'),
    path('cart/update/<int:item_pk>/', update_cart_item_quantity_view, name='update_cart_item_quantity'),
    path('cart/remove/<int:item_pk>/', remove_from_cart_view, name='remove_from_cart'),
]
