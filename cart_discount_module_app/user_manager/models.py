from django.db import models

from django.core.validators import MinValueValidator
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    points = models.IntegerField(default=0, validators=[MinValueValidator(0)])

