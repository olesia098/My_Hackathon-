from multiprocessing.connection import Client
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from client.models import CustomUser

User = get_user_model()


class Comment(models.Model):
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    comments = models.TextField()
    created_ad = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.comments


class Speaker (models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Genre (models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class BooksDescription(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey(CustomUser, related_name='description', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, related_name='description', on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, related_name='description', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    # И ВОТ ЭТИМ ПРОБЛЕМА
    comment = models.ForeignKey(Comment, related_name='description', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class BookContent(models.Model):
    title = models.ForeignKey(BooksDescription, related_name='client', on_delete=models.CASCADE)
    book = models.TextField()


class Rating(models.Model):
    title = models.ForeignKey(BooksDescription, on_delete=models.CASCADE, related_name='rating')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')
    rating = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])


class Like(models.Model):
    author = models.ForeignKey(User,
                            on_delete=models.CASCADE,
                            related_name='like',
                            verbose_name='Владелец лайка'
                                )
    title = models.ForeignKey(BooksDescription,
                            on_delete=models.CASCADE,
                            related_name='like',
                            verbose_name='Продукт'
                                )
    like = models.BooleanField('ЛАААЙК', default=False)

    def __str__(self):
        return f'{self.author}, {self.like}'

