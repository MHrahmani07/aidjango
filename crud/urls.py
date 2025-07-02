# crud/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views 
from book.views import SignUpView, profile_view, home_view, verify_code_view, CustomLoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('book.urls')),
    path('blog/', include('blog.urls')), 
    path('', home_view, name='home'),
    
    # Authentication URLs
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile_view, name='profile'),
    path('verify_code/', verify_code_view, name='verify_code_entry'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
