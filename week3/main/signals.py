from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import *


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
