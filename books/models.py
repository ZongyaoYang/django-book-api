from django.db import models


# Create your models here.
class Author (models.Model):
    name = models.CharField(max_length=200)
    birth_date=models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    
    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="books"
    )
    isbn = models.CharField(max_length=13, unique=True)
    pages = models.PositiveIntegerField()
    published_date = models.DateField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    