from django.urls import path
from . import views
from .views import list_books
from django.contrib.auth import views as auth_views
from .views import RegisterView

urlpatterns = [
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    # Login / Logout
    path('login/', auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    # Registration
    path('register/', RegisterView.as_view(), name='register'),
]

