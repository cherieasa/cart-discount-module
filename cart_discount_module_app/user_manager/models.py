from django.db import models

from django.core.validators import MinValueValidator
from django.contrib.auth.base_user import AbstractBaseUser


class User(AbstractBaseUser):
    points = models.IntegerField(default=0, validators=[MinValueValidator(0)])
