from django.shortcuts import render
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book
from .forms import BookSearchForm

# Create your views here.
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


def book_search(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.none()
    if form.is_valid():
        query = form.cleaned_data['query']
        # Use ORM filtering to safely parameterize queries
        books = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/book_search.html', {'form': form, 'books': books})
