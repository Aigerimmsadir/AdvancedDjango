from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.CharField(max_length=500, default="")

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return '{}: {}'.format(self.id, self.name)


class AdvertisementManager(models.Manager):
    def for_user(self, user):
        return self.filter(owner=user)


class Advertisement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="advertisements")
    image = models.CharField(max_length=500, default="")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="advertisements")

    # objects =AdvertisementManager()
    def __str__(self):
        return '{}: {}'.format(self.name, self.owner)


class Comment(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now=True)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return '{}: {}'.format(self.owner, self.text)
