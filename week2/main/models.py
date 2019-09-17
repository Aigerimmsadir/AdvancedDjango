from django.db import models
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token


class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}: {self.username}'


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    address = models.CharField(max_length=300)
    avatar=models.CharField(max_length=300)
    def __str__(self):
        return self.user.username




class Project(models.Model):
	name=models.CharField(max_length=300)
	descr=models.CharField(max_length=1000)
	creator=models.ForeignKey(MainUser, on_delete=models.CASCADE)




class Block(models.Model):
	TYPES = (
        (0, 'To Do'),
        (1, 'In Process'),
        (2, 'Clone'),
        (3, 'New'),
    )
	name=models.CharField(max_length=300)
	block_type
    gender = models.IntegerField(max_length=1, choices=TYPES)
	project=models.ForeignKey(Project, on_delete=models.CASCADE)