from django.db import models
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token
from .choices import *

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
    avatar = models.FileField()

    def __str__(self):
        return self.user.username


class Project(models.Model):
    name = models.CharField(max_length=300)
    descr = models.CharField(max_length=1000)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE,related_name='created_projects')


class Block(models.Model):
    TO_DO=0
    IN_PROCESS = 1
    DONE = 2
    NEW = 3
    BLOCK_TYPE_CHOICES = (
        (TO_DO, 'To_do'),
        (IN_PROCESS, 'In_process'),
        (DONE, 'Done'),
        (NEW, 'New'),
    )

    name = models.CharField(max_length=300)
    block_type = models.IntegerField(choices=BLOCK_TYPE_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='blocks')


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='project_members')
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE,related_name='involved_projects')


class Task(models.Model):
    name = models.CharField(max_length=300)
    descr = models.CharField(max_length=1000)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE,related_name='created_tasks')
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE,related_name='executed_tasks')
    block = models.ForeignKey(Block, on_delete=models.CASCADE,related_name='blocks')
    order = models.IntegerField()


class TaskDocument(models.Model):
    document = models.FileField()
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE,related_name='task_documents')
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='documents')


class TaskComment(models.Model):
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE,related_name='task_comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='comments')
