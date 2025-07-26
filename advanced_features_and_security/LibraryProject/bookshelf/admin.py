from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.forms import TextInput, Textarea
from django import forms

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns shown in list view
    list_filter = ('publication_year',)                     # Filter sidebar for publication year
    search_fields = ('title', 'author')                     # Search box for title and author

admin.site.register(Book, BookAdmin)

class CustomUserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all required fields, plus repeated password."""
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'profile_photo')

class CustomUserChangeForm(forms.ModelForm):
    """A form for updating users."""
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'profile_photo', 'is_active', 'is_staff', 'is_superuser')

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    list_display = ['username', 'email', 'date_of_birth', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)
