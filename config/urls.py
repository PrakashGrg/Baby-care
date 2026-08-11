from django.contrib import admin
from django.urls import path, include
from apps.users.views_health import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('api/auth/', include('apps.users.urls')),
    path('api/sensors/', include('apps.sensors.urls')),
    path('api/sleep/', include('apps.sleep.urls')),
    path('api/activity/', include('apps.activity.urls')),
    path('api/baby/', include('apps.baby.urls')),
]