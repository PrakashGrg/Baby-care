from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('guardian', 'Guardian'),
        ('caregiver', 'Caregiver'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='parent')
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class PushToken(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='push_tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.token[:20]}...'