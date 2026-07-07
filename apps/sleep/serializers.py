from rest_framework import serializers
from .models import SleepLog


class SleepLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleepLog
        fields = ['id', 'room_name', 'state', 'changed_at']
        read_only_fields = ['id', 'changed_at']