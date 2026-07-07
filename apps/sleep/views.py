from datetime import timedelta
from django.utils import timezone
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.detection.models import MotionEvent
from .models import SleepLog
from .serializers import SleepLogSerializer

SLEEP_THRESHOLD_MINUTES = 5


class CheckSleepStatusView(APIView):
    """
    Infers current sleep/awake state for a room based on recent motion,
    logs a transition if the state changed, and returns the current status.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        room_name = request.query_params.get('room_name', 'default')

        last_motion = MotionEvent.objects.filter(
            room_name=room_name
        ).order_by('-detected_at').first()

        now = timezone.now()
        if last_motion is None:
            inferred_state = 'asleep'
            minutes_since_motion = None
        else:
            minutes_since_motion = (now - last_motion.detected_at).total_seconds() / 60
            inferred_state = 'asleep' if minutes_since_motion >= SLEEP_THRESHOLD_MINUTES else 'awake'

        last_log = SleepLog.objects.filter(room_name=room_name).order_by('-changed_at').first()

        if last_log is None or last_log.state != inferred_state:
            SleepLog.objects.create(
                user=request.user,
                room_name=room_name,
                state=inferred_state
            )

        return Response({
            'room_name': room_name,
            'state': inferred_state,
            'minutes_since_last_motion': round(minutes_since_motion, 2) if minutes_since_motion is not None else None,
        })


class SleepLogListView(generics.ListAPIView):
    """
    Returns sleep/wake transition history for the logged-in user,
    optionally filtered by room via ?room_name=xyz
    """
    serializer_class = SleepLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = SleepLog.objects.filter(user=self.request.user)
        room_name = self.request.query_params.get('room_name')
        if room_name:
            queryset = queryset.filter(room_name=room_name)
        return queryset[:100]