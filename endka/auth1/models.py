from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from utils.upload import *
from utils.validators import *
from django.db.models import Max, Min, Count
from django.db.models import Q


class MainUser(AbstractUser):
    isAdmin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}: {self.username}'



