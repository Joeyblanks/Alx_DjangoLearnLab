from django.contrib import admin
from .models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns shown in list view
    list_filter = ('publication_year',)                     # Filter sidebar for publication year
    search_fields = ('title', 'author')                     # Search box for title and author

admin.site.register(Book, BookAdmin)
