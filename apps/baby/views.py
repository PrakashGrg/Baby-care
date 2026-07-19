from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BabyProfile
from .serializers import BabyProfileSerializer


class BabyProfileViewSet(viewsets.ModelViewSet):
    serializer_class = BabyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BabyProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JoinRoomView(APIView):
    """
    Look up a baby profile by its room_id, for family members
    who want to connect to a room they don't own.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, room_id):
        try:
            baby = BabyProfile.objects.get(room_id=room_id)
        except BabyProfile.DoesNotExist:
            return Response({'error': 'No baby profile found with that room code.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BabyProfileSerializer(baby).data)