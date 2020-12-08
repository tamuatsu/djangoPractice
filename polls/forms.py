from django.forms import ModelForm
from . import models

class AuthorForm(ModelForm):
    class Meta:
        model = models.Author
        fields = ['name', 'title', 'birth_date']

class BookForm(ModelForm):
    class Meta:
        model = models.Book
        fields = ['name', 'authors']