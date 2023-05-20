from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# import managers
from .managers import UserManager

class Interest(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Interest',
        blank=False
    )
    description = models.TextField(
        verbose_name='Description',
        blank=False
    )

    class Meta:
        verbose_name = 'Interest'
        verbose_name_plural = 'Interests'
    
    def __str__(self):
        return str(self.id) +' - '+ self.name

class User(AbstractBaseUser, PermissionsMixin):

    OCUPATION_CHOICES = (
        ('A', 'Administrator'),
        ('W', 'Worker'),
        ('U', 'User'),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField('Full name', max_length=100)
    ocupation = models.CharField(
        'Ocupation',
        max_length=1,
        choices=OCUPATION_CHOICES,
        default='U'
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    code_register = models.CharField('Register Code', max_length=6, blank=True, null=True)

    interests = models.ManyToManyField(Interest, verbose_name='Interests', blank=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['full_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return str(self.id) +' - '+self.full_name





