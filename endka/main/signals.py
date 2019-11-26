from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from main.models import *

from utils.upload import image_delete_path


@receiver(pre_delete, sender=Article)
def article_deleted(sender, instance, **kwargs):
    print(instance)
    imgs = instance.images.all()
    bool(imgs)
    print(imgs)
    for img in imgs:
        print(img)
        image_delete_path(image=img.image)


@receiver(post_save, sender=Article)
def project_created(sender, instance, created, **kwargs):
    if created:
        user = MainUser.objects.get(id=3)
        f = FavoriteArticle.objects.create(article=instance, user=user)
        print(f)
