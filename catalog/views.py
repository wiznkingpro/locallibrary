from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book, Author, BookInstance, Genre

# catalog/views.py
from django.shortcuts import render
from .models import Book, BookInstance, Author

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'catalog/index.html', context)  # ← ВАЖНО: путь с префиксом!


class BookListView(ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'

class BookDetailView(DetailView):  # ← ОБЯЗАТЕЛЬНО добавьте этот класс
    model = Book
    template_name = 'catalog/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # ✅ Правильно!
        # Если нужно добавить что-то в контекст — делайте это здесь
        return context

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'



