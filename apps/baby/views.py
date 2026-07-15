from rest_framework import viewsets, permissions
from .models import BabyProfile
from .serializers import BabyProfileSerializer


class BabyProfileViewSet(viewsets.ModelViewSet):
    serializer_class = BabyProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BabyProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)