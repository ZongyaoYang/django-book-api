from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [  # noqa: RUF012
            "id",
            "title",
            "author",
            "isbn",
            "pages",
            "published_date",
            "is_available",
            "created_at",
        ]
        read_only_fields = ["created_at"]  # noqa: RUF012
