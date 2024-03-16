import random

from django.contrib.auth.models import AbstractUser
from django.db import models

from service.models import NULLABLE

random_code = str(random.randint(00000000, 99999999))


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    phone = models.CharField(max_length=35, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='Страна', **NULLABLE)
    verification_code = models.CharField(max_length=8, default=random_code,
                                         verbose_name='Код подтверждения почты', **NULLABLE)
    is_active = models.BooleanField(default=False, verbose_name='Активность')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
