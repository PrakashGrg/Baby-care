from rest_framework import serializers
from .models import BabyProfile


class BabyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BabyProfile
        fields = ['id', 'name', 'birthday', 'weight_kg', 'height_cm', 'sleep_goal_hours', 'photo_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']