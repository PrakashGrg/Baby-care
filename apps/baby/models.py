import uuid
from django.db import models
from django.conf import settings


def generate_room_id():
    return uuid.uuid4().hex[:8]


class BabyProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='babies')
    name = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)
    height_cm = models.FloatField(null=True, blank=True)
    sleep_goal_hours = models.FloatField(default=12.0)
    photo_url = models.URLField(blank=True)
    room_id = models.CharField(max_length=16, unique=True, default=generate_room_id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name