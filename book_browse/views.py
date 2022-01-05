from django.db import models
from django.shortcuts import render, redirect
import requests
from django.views.generic import ListView
import environ
from .forms import BookSearch
from .models import Book, Author, BookInstance
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required

# from .forms import RenewBookForm
from book_browse.forms import RenewBookForm

env = environ.Env()
env.read_env()  # reading .env file

key = env.str('API_KEY')


def index(request):
    form = BookSearch()
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
 
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  
    return render(request, 'index.html', context={'form': form, 'num_books':num_books,'num_instances':num_instances,
    'num_instances_available':num_instances_available,'num_authors':num_authors})

def books(request):

    author = request.GET.get('author', False)
    search = author if request.GET.get(
        'search', False) == "" else request.GET.get('search', False)

    if (search == False and author == False) or (search == "" and author == ""):
        return redirect('/')

    queries = {'q': search, 'inauthor': author, 'key': key}
    print(queries)
    r = requests.get(
        'https://www.googleapis.com/books/v1/volumes?', params=queries)
    print(r)
    if r.status_code != 200:
        return render(request, 'book_browse/books.html', {'message': 'Извините, похоже, сейчас возникла проблема с Google Книгами.'})

    data = r.json()

    if not 'items' in data:
        return render(request, 'book_browse/books.html', {'message': 'Извините, ни одна книга не соответствует этому поисковому запросу.'})

    fetched_books = data['items']
    books = []
    for book in fetched_books:
        book_dict = {
            'title': book['volumeInfo']['title'],
            'image': book['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in book['volumeInfo'] else "Изображение не найдено",
            'authors': ", ".join(book['volumeInfo']['authors']) if 'authors' in book['volumeInfo'] else "Неизвестен",
            'publisher': book['volumeInfo']['publisher'] if 'publisher' in book['volumeInfo'] else "Неизвестно",
            'info': book['volumeInfo']['infoLink'],
            'popularity': book['volumeInfo']['ratingsCount'] if 'ratingsCount' in book['volumeInfo'] else 0
        }
        books.append(book_dict)

    def sort_by_pop(e):
        return e['popularity']

    books.sort(reverse=True, key=sort_by_pop)

    return render(request, 'book_browse/books.html', {'books': books})

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context
        
class BookDetailView(generic.DetailView):
    model = Book
    def book_detail_view(request, primary_key):
        book = get_object_or_404(Book, pk=primary_key)
        return render(request, 'book_browse/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class AuthorDetailView(generic.DetailView):
    model = Author
    def author_detail_view(request, primary_key):
        author = get_object_or_404(Author, pk=primary_key)
        return render(request, 'book_browse/author_detail.html', context={'author': author})

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='book_browse/arenda.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).order_by('due_back')

@login_required

def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.borrower = request.user
            book_instance.save()
            return HttpResponseRedirect(reverse('my-borrowed'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_browse/book_reniew.html', context)


class ArendovatView(generic.ListView):
    model = BookInstance
    template_name = 'book_browse/arendovat.html'