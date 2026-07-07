from django.db import models
from django.conf import settings


class SleepLog(models.Model):
    STATE_CHOICES = (
        ('asleep', 'Asleep'),
        ('awake', 'Awake'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100)
    state = models.CharField(max_length=10, choices=STATE_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f'{self.room_name}: {self.state} at {self.changed_at}'