from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.shared.models import AbstractBaseModel


class User(AbstractUser, AbstractBaseModel):
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    birth_date = models.DateField(null=True, blank=True)
    slug = models.SlugField(unique=True)
