from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', "O'quvchi"),
        ('teacher', "O'qituvchi"),
        ('admin', "Admin"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    is_approved = models.BooleanField(default=False, verbose_name="Tasdiqlangan")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username