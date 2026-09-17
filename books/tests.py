from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book

# Create your tests here.


class BookAPITest(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Frank Herbert")
        self.book = Book.objects.create(
            title="Dune",
            author=self.author,
            isbn="9780441172719",
            pages=412,
            published_date="1965-08-01",
        )
        
    def test_list_books(self):
        response = self.client.get("/api/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
