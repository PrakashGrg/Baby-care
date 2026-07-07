from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Avg, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from apps.detection.models import MotionEvent
from apps.audio.models import CryEvent
from apps.sensors.models import SensorReading
from apps.sleep.models import SleepLog


class DailySummaryView(APIView):
    """
    Returns an aggregated activity summary for a room on a given day.
    Query params: room_name (default 'default'), date (YYYY-MM-DD, default today)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        room_name = request.query_params.get('room_name', 'default')
        date_str = request.query_params.get('date')

        if date_str:
            try:
                day = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'date must be in YYYY-MM-DD format'}, status=400)
        else:
            day = timezone.now().date()

        start = timezone.make_aware(datetime.combine(day, datetime.min.time()))
        end = start + timedelta(days=1)

        motion_qs = MotionEvent.objects.filter(
            room_name=room_name, detected_at__gte=start, detected_at__lt=end
        )
        cry_qs = CryEvent.objects.filter(
            room_name=room_name, detected_at__gte=start, detected_at__lt=end
        )
        sensor_qs = SensorReading.objects.filter(
            room_name=room_name, recorded_at__gte=start, recorded_at__lt=end
        )
        sleep_qs = SleepLog.objects.filter(
            room_name=room_name, changed_at__gte=start, changed_at__lt=end
        ).order_by('changed_at')

        sensor_averages = sensor_qs.aggregate(
            avg_temp=Avg('temperature_celsius'),
            avg_humidity=Avg('humidity_percent'),
        )

        sleep_transitions = [
            {'state': log.state, 'changed_at': log.changed_at}
            for log in sleep_qs
        ]

        return Response({
            'room_name': room_name,
            'date': str(day),
            'motion_event_count': motion_qs.count(),
            'cry_event_count': cry_qs.count(),
            'sensor_reading_count': sensor_qs.count(),
            'average_temperature_celsius': round(sensor_averages['avg_temp'], 1) if sensor_averages['avg_temp'] else None,
            'average_humidity_percent': round(sensor_averages['avg_humidity'], 1) if sensor_averages['avg_humidity'] else None,
            'sleep_transitions': sleep_transitions,
        })