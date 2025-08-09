from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, Author
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

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
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        login_successful = self.client.login(username='testuser', password='testpass123')
        self.assertTrue(login_successful)

