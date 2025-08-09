from django.db import models

# Create your models here.
class Author(models.Model):
    # The author's name
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    # Title of the book
    title = models.CharField(max_length=255)
    # Year the book was published
    publication_year = models.IntegerField()
    # ForeignKey relationship to Author model (many books can belong to one author)
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
