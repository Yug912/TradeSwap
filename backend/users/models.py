from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Account data that belongs to a TradeSwap user."""

    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username
