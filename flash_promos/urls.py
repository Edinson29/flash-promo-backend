from rest_framework.routers import DefaultRouter
from .views import FlashPromoViewSet

router = DefaultRouter()
router.register(r"flash-promos", FlashPromoViewSet, basename="flashpromo")

urlpatterns = router.urls
