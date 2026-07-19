from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BabyProfileViewSet, JoinRoomView

router = DefaultRouter()
router.register('', BabyProfileViewSet, basename='baby-profile')

urlpatterns = [
    path('join/<str:room_id>/', JoinRoomView.as_view(), name='join-room'),
] + router.urls