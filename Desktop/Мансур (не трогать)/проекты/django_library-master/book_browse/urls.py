from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path("", views.index, name='index'),

    path('books/', views.books, name='books'),
    path('bookslist/', views.BookListView.as_view(), name='bookslist'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),

    path('authors/', views.AuthorListView.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(),
        name='author-detail'),

    path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(),
         name='my-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian,
         name='renew-book-librarian'),
    path('arend/', views.ArendovatView.as_view(), name='arend'),
]
