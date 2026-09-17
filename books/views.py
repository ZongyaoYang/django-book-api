from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["post"])
    def mark_unavailable(self, request, pk=None):
        book = self.get_object()
        book.is_available = False
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def list_available(self, request):
        available_books = self.get_queryset().filter(is_available=True)
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
