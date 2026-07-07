from django.urls import path
from .views import CheckSleepStatusView, SleepLogListView

urlpatterns = [
    path('status/', CheckSleepStatusView.as_view(), name='sleep-status'),
    path('history/', SleepLogListView.as_view(), name='sleep-history'),
]