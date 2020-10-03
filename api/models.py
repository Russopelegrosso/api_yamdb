import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class UserRole(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    email = models.EmailField('Почта', unique=True, blank=False)
    role = models.CharField('Статус', max_length=20, choices=UserRole.choices,
                            default=UserRole.USER)
    bio = models.TextField('Профиль', max_length=200, blank=True)

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN or self.is_staff


class Category(models.Model):
    name = models.CharField('Имя', max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Имя', max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=100, db_index=True)
    year = models.PositiveSmallIntegerField(
        'Год выпуска', blank=True,
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(datetime.date.today().year)
        ]
        , db_index=True
    )

    description = models.TextField(
        'Описание', blank=True, default=''
    )
    genre = models.ManyToManyField(
        Genre, related_name='titles',
        verbose_name='жанр', blank=True, db_index=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles',
        verbose_name='категория', blank=True, null=True, db_index=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведения')
    text = models.TextField(verbose_name='Отзыв')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews', verbose_name='Автор')
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        verbose_name='Рейтинг')
    pub_date = models.DateTimeField('Дата публикации отзыва',
                                    auto_now_add=True,
                                    db_index=True)

    def __str__(self):
        return self.text

    class Meta:
        unique_together = ['title', 'author']
        ordering = ['pub_date']


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Автор')
    reviews = models.ForeignKey(Review, on_delete=models.CASCADE,
                                related_name='comments', verbose_name='Отзыв')
    pub_date = models.DateTimeField('Дата добавления комментария',
                                    auto_now_add=True,
                                    db_index=True)

    class Meta:
        ordering = ['pub_date']
