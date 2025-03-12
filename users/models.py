from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, verbose_name="Имя", blank=True, unique=False)
    last_name = None
    first_name = None
    email = models.EmailField(unique=True)
    token_for_activate = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    phone = models.CharField(max_length=15, verbose_name="Телефон", blank=True, unique=False)
    country = models.CharField(max_length=15, verbose_name="Страна", blank=True, unique=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    @property
    def user_is_active(self):
        return self.is_active
