from django.db import models
from django.urls import reverse
import uuid
from django.conf import settings
from datetime import date


class Genre(models.Model):
    """Модель, представляющая книжный жанр."""
    name = models.CharField(
        max_length=200,
        help_text="Введите жанр книги (например, Фантастика, Поэзия и т.д.)"
    )

    def __str__(self):
        return self.name


class Author(models.Model):
    """Модель, представляющая автора."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Умер', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Book(models.Model):
    """Модель, представляющая книгу (не конкретный экземпляр)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text="Краткое описание книги")
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        help_text='13-значный <a href="https://www.isbn-international.org/content/what-isbn">ISBN</a>'
    )
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр(ы) для этой книги")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])


class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Уникальный ID для конкретного экземпляра книги во всей библиотеке"
    )
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )  # ← ВНУТРИ класса!
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Техобслуживание'),
        ('o', 'Выдана'),
        ('a', 'Доступна'),
        ('r', 'Зарезервирована'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Доступность книги'
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)


