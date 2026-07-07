from django.db import models
from django.conf import settings


class SensorReading(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=100)
    temperature_celsius = models.FloatField()
    humidity_percent = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f'{self.room_name}: {self.temperature_celsius}°C, {self.humidity_percent}% at {self.recorded_at}'