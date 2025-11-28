from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance
from django.contrib.auth.mixins import LoginRequiredMixin

# ===== Главная страница (Часть 5) =====
def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()

    # Счётчик посещений (Часть 7)
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    return render(request, 'catalog/index.html', context)


# ===== Список книг (Часть 6) =====
class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'
    paginate_by = 10


# ===== Детали книги =====
class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'


# ===== Список авторов =====
class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'
    paginate_by = 10


# ===== Детали автора =====
class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'




class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

