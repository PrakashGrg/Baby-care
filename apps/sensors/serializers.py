from rest_framework import serializers
from .models import SensorReading


class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = ['id', 'room_name', 'temperature_celsius', 'humidity_percent', 'recorded_at']
        read_only_fields = ['id', 'recorded_at']