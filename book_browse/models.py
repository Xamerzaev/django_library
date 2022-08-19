from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date


class Post(models.Model):
    email = models.EmailField('Email', max_length=254)

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Genre(models.Model):
    name = models.CharField(max_length=200,
                            help_text="Введите жанр книги \
                        (например: фантастика, приключение, детектив и т.д.)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000,
                               help_text="Введите краткое описание книги")
    isbn = models.CharField('ISBN', max_length=13,
                            help_text='13 символов <a href=\
                            "https://www.isbn-international.org/content/what-isbn"\
                            >ISBN number</a>')
    genre = models.ManyToManyField(Genre,
                                   help_text="Выберите жанр для этой книги")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Уникальный идентификатор\
                          для этой конкретной книги во всей библиотеке")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField("Импринт", max_length=200)
    due_back = models.DateField('Дата возвращения', null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Поддержка'),
        ('o', 'Забронирована'),
        ('a', 'Свободная'),
        ('r', 'Занята'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m',
                              help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)
        verbose_name = 'Экземпляр книги'
        verbose_name_plural = 'Экземпляры книг'

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return '%s (%s)' % (self.id, self.book.title)


class Author(models.Model):
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True)
    date_of_death = models.DateField('Дата смерти', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
