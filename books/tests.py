from typing import cast

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

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

    def test_list_books_returns_correct_data(self):
        response = cast(Response, self.client.get("/api/books/"))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.data is not None
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["title"], "Dune")
        self.assertEqual(results[0]["author"]["name"], "Frank Herbert")

    def test_create_book_requires_authentication(self):
        payload = {
            "title": "Dune Messiah",
            "author_id": self.author.pk,
            "isbn": "9780441172818",
            "pages": 256,
            "published_data": "1969-10-01",
        }

        response = self.client.post("/api/books/", payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_when_authenticated(self):
        user = User.objects.create_user(username="tester", password="testpass123")
        self.client.force_authenticate(user=user)

        payload = {
            "title": "Dune Messiah",
            "author_id": self.author.pk,
            "isbn": "9780441172818",
            "pages": 256,
            "published_date": "1969-10-01",
        }
        
        response = self.client.post("/api/books/", payload)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        
    def test_mark_unavailable(self):
        user = User.objects.create_user(username="tester2", password="testpass123")
        self.client.force_authenticate(user=user)
        
        url = f"/api/books/{self.book.id}/mark_unavailable/"
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertFalse(self.book.is_available)
        
        
    def test_list_available_excludes_unavailable_books(self):
        Book.objects.create(
            title="Children of Dune",
            author=self.author,
            isbn="9780441104024",
            pages=555,
            published_date="1976-04-01",
            is_available=False,
        )
        
        response = self.client.get("/api/books/list_available/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertIn("Dune", titles)
        self.assertNotIn("Children of Dune", titles)
        