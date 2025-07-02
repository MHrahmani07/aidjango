# book/urls.py

from django.urls import path
from .views import BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, toggle_favorite_view,get_random_book_api

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('new/', BookCreateView.as_view(), name='book_create'),
    path('<int:pk>/edit/', BookUpdateView.as_view(), name='book_update'),
    path('<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('<int:pk>/toggle_favorite/', toggle_favorite_view, name='toggle_favorite'),
    path('api/random-book/', get_random_book_api, name='random_book_api'),
]
 