from django.db import models
from django.conf import settings


class MotionEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100)
    detected_at = models.DateTimeField(auto_now_add=True)
    motion_score = models.FloatField(default=0.0)

    class Meta:
        ordering = ['-detected_at']

    def __str__(self):
        return f'Motion in {self.room_name} at {self.detected_at}'