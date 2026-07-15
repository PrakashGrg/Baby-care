from rest_framework.routers import DefaultRouter
from .views import BabyProfileViewSet

router = DefaultRouter()
router.register('', BabyProfileViewSet, basename='baby-profile')

urlpatterns = router.urls