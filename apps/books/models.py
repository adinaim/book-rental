from distutils.command.upload import upload
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from slugify import slugify
from uuid import uuid4
import random

from .utils import get_time


User = get_user_model()

class Book(models.Model):   # можно создать только если книга есть в базе данных, иначе проверка модераторами (прописать проверку в отдельном файле)      many to many:   человек, книга 3 таблица

    STATUS_CHOICES = (
        ('available', 'Доступна'),
        ('rented', 'Занята')
    )
    
    title = models.CharField(max_length=150, required=True)
    author = models.CharField(max_length=150, requied=True)
    slug = models.SlugField(max_length=200, primary_key=True, blank=True)
    description = models.TextField()
    image_link = models.ImageField(upload_to='book_images', default=...)       # подготовить дефолтную фотку
    status = models.CharField(
        max_length=12, 
        choices=STATUS_CHOICES,
        default='unknown'
    )
    genre = models.ManyToManyField(
        to='Genre',
        related_name='genre',
        blank=True
    )
    number_of_copies = models.SmallIntegerField(required=True)



    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('created_at', )    # что за created at

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})     # вспомнить для чего


class Genre(models.Model):                                        # many to many, как это реализовать
    GENRE_CHOICES=...

    genre = models.CharField(max_length=30, unique=True, choices=...)          # не будут ли конфликтовать
    slug = models.SlugField(primary_key=True, blank=True, max_length=35)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.user.username} to {self.book.title}'


class Rating(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE =5
    RATING_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='ratings'
    )

    def __str__(self) -> str:
        return str(self.rating)


class LikeToBook(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='books-likes'
    )

    def __str__(self):
        return f'Liked by {self.user.username}'


class LikeToComment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='likes'
    )
    comment = models.ForeignKey(
        to=Comment,
        on_delete=models.CASCADE,
        related_name='comments-likes'
    )

    def __str__(self):
        return f'Liked by {self.user.username}'


class Reservation(models.Model):
    STATUS_RENTED = 0
    STATUS_AVAILABLE = 1
    STATUS_RESERVED = -1
    STATUS_TYPES = [
        (STATUS_RENTED, "Арендована"),
        (STATUS_AVAILABLE, "Доступна"),
    ]

    rent_id = models.UUIDField(     # преобразовать в qr, чтобы при передаче списалась сумма и поменялся статус
        default=uuid4,
        primary_key=True,
        editable=False
    )
    book = models.ForeignKey(
        to=Book,
        related_name="reservations",
        on_delete=models.CASCADE
    )
    renter = models.ForeignKey(   # тот кто дает в аренду
        to=User,
        related_name="requesting-reservations",
        on_delete=models.CASCADE
    )
    invitees = models.ManyToManyField(
        to=User,
        through="ReservationInvitee"
    )
    title = models.CharField(max_length=150)
    status = models.IntegerField(
        choices=STATUS_TYPES,
        default=STATUS_AVAILABLE
    )
    date_from = models.DateTimeField()    # проверка, чтобы не в прошлом, проверки, чтобы не было занято, проверка, чтобы были запасные дни, чтобы передать книгу
    date_to = models.DateTimeField()      # проверка, чтобы не больше, чем на месяц


class ReservationConfirmation(models.Model):
    IS_PENDING = -1
    IS_GIVING = 1
    IS_NOT_GIVING = 0
    ATTENDING_STATUSES = [
        (IS_PENDING, "Pending"),
        (IS_GIVING, "Giving"),
        (IS_NOT_GIVING, "Not giving")
    ]

    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE
    )
    employee = models.ForeignKey(
        User,
        related_name="invited_reservations",
        on_delete=models.CASCADE
    )
    status = models.IntegerField(
        choices=ATTENDING_STATUSES,
        default=IS_PENDING
    )


# как работают лайки на комменты: обхединить лайки на книги и комменты? 


# человек сам выбирает на сколько дней взять, можно забронировать наперед, оплата списываеися только если нкигу взяли

# комментарии арендатору, как пользовался, вовремя ли вернул, если посутпит 3 жалобы, нельзя будт пользоваться сервисом


# для библиотеки, в ее базе есть книги, их можно бронировать,  количество доступных копий (как добавить - для проекта просто рандомный сделаю)

# тг бот, помогает найти, есть ли такая книга, когда будет свободна, режим работы библиотеки, выводит список книг, которые ты должен сдать в какие даты