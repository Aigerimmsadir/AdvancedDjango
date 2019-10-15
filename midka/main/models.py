from django.db import models
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token


class MainUser(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_login}'

    def __str__(self):
        return f'{self.id}: {self.username}'


class Profile(models.Model):
    SUPER_ADMIN = 0
    STORE_ADMIN = 1
    GUEST = 2
    ROLE_CHOICES = (
        (SUPER_ADMIN, 'super_admin'),
        (STORE_ADMIN, 'store_admin'),
        (GUEST, 'guest'),
    )
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE, related_name='profile')
    role = models.IntegerField(choices=ROLE_CHOICES, default=GUEST)

    def __str__(self):
        return self.user.username


class ProductServiceBase(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}( {self.price} tg)'


class Product(ProductServiceBase):
    FOOD = 0
    CLOTHES = 1
    DEVICES = 2
    PRODUCT_TYPE_CHOICES = (
        (FOOD, 'food'),
        (CLOTHES, 'clothes'),
        (DEVICES, 'devices'),
    )
    size = models.IntegerField()
    type = models.IntegerField(choices=PRODUCT_TYPE_CHOICES)
    existence = models.BooleanField(default=True)

    class Meta(ProductServiceBase.Meta):
        unique_together = ('name', 'price')


class Service(ProductServiceBase):
    STANDART_DELIVERY = 0
    EXPRESS_DELIVERY = 1

    SERVICE_TYPE_CHOICES = (
        (STANDART_DELIVERY, 'standart_delivery'),
        (EXPRESS_DELIVERY, 'express_delivery'),
    )
    approximate_duration = models.IntegerField()
    type = models.IntegerField(choices=SERVICE_TYPE_CHOICES)

    class Meta(ProductServiceBase.Meta):
        unique_together = ('type', 'price')
