from django.db import models
from auth1.models import MainUser
from utils.constants import *
from utils.upload import *
from utils.validators import *


class Article(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2550)
    price = models.IntegerField()
    city = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    color = models.PositiveSmallIntegerField(choices=COLOR_CHOICES)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='articles')

    def __str__(self):
        return f'{self.creator}: {self.id} {self.name}'


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=image_path, validators=[image_size, image_extension],
                              null=True)


class FavoriteArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='favorite_articles')
