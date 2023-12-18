from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

from django.contrib.auth.models import BaseUserManager


class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # objects = CustomUserManager()

    def __str__(self):
        return str(self.username)
