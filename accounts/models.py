from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    fullname = models.CharField(
        max_length=100, null=True, blank=False, help_text="Full name"
    )
    email = models.EmailField(
        verbose_name="Email Address", unique=True, help_text="Email address"
    )
    created_at = models.DateTimeField(auto_now_add=True)
