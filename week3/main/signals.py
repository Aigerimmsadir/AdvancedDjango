from django.db.models.signals import post_save,pre_delete,post_delete
from django.dispatch import receiver

from main.models import *

from utils.upload import file_delete_path


@receiver(pre_delete, sender=Task)
def task_deleted(sender, instance, **kwargs):
    docs = TaskDocument.objects.filter(task=instance)
    bool(docs)
    for taskdocument in docs:
        print(taskdocument)
        file_delete_path(document=taskdocument.document)


@receiver(post_save, sender=MainUser)
def user_created(sender, instance, created, **kwargs):
    if created:
        print('here')
        Profile.objects.create(user=instance)
    print(instance)


@receiver(post_save, sender=Project)
def project_created(sender, instance, created, **kwargs):
    if created:
        Block.objects.create(name='To do',block_type=0,project=instance)
        Block.objects.create(name='In process', block_type=1, project=instance)
        Block.objects.create(name='Done', block_type=2, project=instance)
        print(instance.blocks)


@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    if instance.avatar:
        file_delete_path(instance.avatar)