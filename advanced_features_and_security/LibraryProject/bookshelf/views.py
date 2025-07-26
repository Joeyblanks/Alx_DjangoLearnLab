from django.shortcuts import render
from django.contrib.auth.decorators import permission_required, login_required

# Create your views here.
@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    # view logic
    pass
