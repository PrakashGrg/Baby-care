import random
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SensorReading
from .serializers import SensorReadingSerializer


class SimulateSensorReadingView(APIView):
    """
    Generates a simulated temperature/humidity reading for a room,
    saves it, and returns it. Call this periodically (e.g. every
    30-60s from the app) to build up a realistic history.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        room_name = request.data.get('room_name', 'default')

        # Realistic baby-room ranges
        temperature = round(random.uniform(20.0, 26.0), 1)
        humidity = round(random.uniform(40.0, 60.0), 1)

        reading = SensorReading.objects.create(
            user=request.user,
            room_name=room_name,
            temperature_celsius=temperature,
            humidity_percent=humidity,
        )
        return Response(SensorReadingSerializer(reading).data, status=201)


class SensorReadingListView(generics.ListAPIView):
    """
    Returns sensor reading history for the logged-in user,
    optionally filtered by room via ?room_name=xyz
    """
    serializer_class = SensorReadingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = SensorReading.objects.filter(user=self.request.user)
        room_name = self.request.query_params.get('room_name')
        if room_name:
            queryset = queryset.filter(room_name=room_name)
        return queryset[:100]