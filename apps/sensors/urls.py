from django.urls import path
from .views import SimulateSensorReadingView, SensorReadingListView

urlpatterns = [
    path('simulate/', SimulateSensorReadingView.as_view(), name='simulate-sensor'),
    path('history/', SensorReadingListView.as_view(), name='sensor-history'),
]