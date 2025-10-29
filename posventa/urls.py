from rest_framework.routers import DefaultRouter
from .views import ReturnViewSet, WarrantyViewSet

router = DefaultRouter()
router.register(r'devoluciones', ReturnViewSet)
router.register(r'garantias', WarrantyViewSet)

urlpatterns = router.urls
