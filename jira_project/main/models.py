from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from utils.upload import *
from utils.validators import *
from django.db.models import Max, Min, Count
from django.db.models import Q
from main.managers import *


class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.id}: {self.username}'


class Profile(models.Model):
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, null=True)
    address = models.CharField(max_length=300, null=True)
    avatar = models.FileField(upload_to=avatar_document_path,
                              validators=[task_document_size, avatar_document_extension],
                              null=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    name = models.CharField(max_length=300)
    descr = models.CharField(max_length=1000)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='created_projects')
    objects = models.Manager()
    projects = ProjectManager()

    @property
    def project_member_count(self):
        return self.project_members.count()

    def __str__(self):
        return self.name


class Block(models.Model):
    TO_DO = 0
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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='blocks')

    @property
    def tasks_count(self):
        return self.blocks.count()

    def __str__(self):
        return f'{self.name}({self.project})'


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_members')
    user = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='involved_projects')
    objects = models.Manager()
    members=ProjectMemberManager()
    def __str__(self):
        return self.user.username


class Task(models.Model):
    name = models.CharField(max_length=300)
    descr = models.CharField(max_length=1000)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='created_tasks')
    executor = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='executed_tasks')
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='tasks')
    order = models.IntegerField()
    objects = models.Manager()
    tasks = TaskManager()

    def __str__(self):
        return f'Task {self.id} "{self.name}"({self.creator})'


class TaskDocument(models.Model):
    document = models.FileField(upload_to=task_document_path, validators=[task_document_size, task_document_extension],
                                null=True)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='task_documents')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return f'{self.task}(document #){self.id}'


class TaskComment(models.Model):
    body = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='task_comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    stars = models.PositiveSmallIntegerField(default=0)
    objects = models.Manager()
    comments = TaskCommentManager()

    def __str__(self):
        return f'{self.body}({self.creator})'

    def save(self, *args, **kwargs):
        created = self.pk is None
        if created:
            if self.creator.is_superuser:
                self.stars = 10
        super().save(*args, **kwargs)
