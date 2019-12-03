from django.db import models
from main.models import *
from django.db.models import Max, Min, Count
from django.db.models import Q


class ProjectManager(models.Manager):
    def filter_by_name(self, name):
        return super(ProjectManager, self).get_queryset().filter(name__contains=name)

    def my_projects(self, user):
        return super(ProjectManager, self).get_queryset().filter(creator=user)

    def more_than_2_members(self):
        return super(ProjectManager, self).get_queryset(project_member_count__gt=2)

    def order_by_name(self):
        return super(ProjectManager, self).get_queryset().order_by('name')


class TaskManager(models.Manager):
    def tasks_with_media(self):
        return super().get_queryset().annotate(Count('documents')).filter(documents__count__gt=0)

    def tasks_for_me(self, user):
        return super().get_queryset().filter(Q(creator=user) | Q(executor=user))

    def my_tasks(self, user):
        return super().get_queryset().filter(creator=user)

    def tasks_to_execute(self, user):
        return super().get_queryset().filter(creator=user)


class TaskCommentManager(models.Manager):
    def my_comments(self, user):
        return super().get_queryset().filter(creator=user)

    def my_comments_ordered(self, user):
        return super().get_queryset().filter(creator=user)

    def ordered_popularity(self):
        return super().get_queryset().order_by('-stars')

    def comments_to_my_tasks(self, user):
        return super().get_queryset().filter(task_id__in=user.created_tasks.values_list('id'))


class ProjectMemberManager(models.Manager):
    def sort_by_user_last_name(self):
        return super().get_queryset().order_by('user__last_name')

    def projects_of_user(self, user):
        return super().get_queryset().filter(user=user)
