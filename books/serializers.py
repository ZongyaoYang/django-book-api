from rest_framework import serializers

from .models import Author, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "birth_date", "bio"]


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author", write_only=True
    )

    class Meta:
        model = Book
        fields = [  # noqa: RUF012
            "id",
            "title",
            "author",
            "author_id",
            "isbn",
            "pages",
            "published_date",
            "is_available",
            "created_at",
        ]
        read_only_fields = ["created_at"]  # noqa: RUF012
