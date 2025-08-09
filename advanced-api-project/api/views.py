from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, Author
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your views here.
# Permissions: Read-only access for everyone, but create/update/delete is restricted to authenticated users

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # Allow read-only access to anyone (no permission classes)
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', 'author__name']
    ordering_fields = ['publication_year', 'title']
     # Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Allow filtering by these fields
    filterset_fields = ['title', 'author__name', 'publication_year']

    # Enable search for these fields (text search)
    search_fields = ['title', 'author__name']

    # Allow ordering by these fields
    ordering_fields = ['title', 'publication_year']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

  def perform_create(self, serializer):
        # For example, you can attach the current user here if needed
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create author and book data once
        author = Author.objects.create(name="Test Author")
        cls.book = Book.objects.create(title="Test Book", publication_year=2020, author=author)

        # Create and authenticate user
        cls.user = User.objects.create_user(username='testuser', password='testpass123')
        cls.token = Token.objects.create(user=cls.user)

    def test_list_books(self):
        url = reverse('book-list')  # Assuming you named this URL path 'book-list'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_book_authenticated(self):
        url = reverse('book-create')  # Assuming this name for create view
        data = {
            "title": "New Book",
            "publication_year": 2019,
            "author": self.book.author.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Book")

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {
            "title": "No Auth Book",
            "publication_year": 2018,
            "author": self.book.author.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book(self):
        url = reverse('book-update', args=[self.book.id])
        data = {
            "title": "Updated Title",
            "publication_year": 2020,
            "author": self.book.author.id
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Updated Title")

    def test_delete_book(self):
        url = reverse('book-delete', args=[self.book.id])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_filter_books_by_title(self):
        url = reverse('book-list') + '?title=Test Book'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for book in response.data:
            self.assertIn("Test Book", book['title'])

    def test_search_books(self):
        url = reverse('book-list') + '?search=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any("Test" in book['title'] for book in response.data))

    def test_order_books(self):
        # Assuming multiple books; since we only have one, this is a minimal test
        url = reverse('book-list') + '?ordering=title'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_access_restrictions(self):
        # Try to update without auth
        url = reverse('book-update', args=[self.book.id])
        data = {"title": "Unauthorized Update"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
