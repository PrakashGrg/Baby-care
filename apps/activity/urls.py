from django.urls import path
from .views import DailySummaryView, EventTimelineView

urlpatterns = [
    path('daily-summary/', DailySummaryView.as_view(), name='daily-summary'),
    path('timeline/', EventTimelineView.as_view(), name='event-timeline'),
]