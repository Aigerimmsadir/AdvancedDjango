from django.db import models
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework.authtoken.models import Token


class Company(models.Model):
    name = models.CharField(max_length=255)


class Department(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')


class MainUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class MainUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = []

    objects = MainUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Profile(models.Model):
    last_name = models.CharField(max_length=255, null=True)
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_employees')
    is_head = models.BooleanField(default=False)

    @property
    def company(self):
        return self.department.company

    @property
    def head(self):
        return Profile.objects.get(department=self.department, is_head=True)

    def __str__(self):
        return self.last_name


class Report(models.Model):
    author = models.ForeignKey(MainUser, on_delete=models.CASCADE, related_name='reports')
    text = models.CharField(max_length=255)
    date_from = models.DateTimeField(auto_now=True)
    date_to = models.DateTimeField()
