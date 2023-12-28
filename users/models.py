from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """ Модель пользователя сервисом """

    username = None

    email = models.EmailField(_("email"), unique=True)
    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['last_name']
