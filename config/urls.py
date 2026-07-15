from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/sensors/', include('apps.sensors.urls')),
    path('api/sleep/', include('apps.sleep.urls')),
    path('api/activity/', include('apps.activity.urls')),
    path('api/baby/', include('apps.baby.urls')),
]