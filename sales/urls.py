from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartViewSet, CheckoutView, PaymentView, OrderViewSet

router = DefaultRouter()
router.register(r'carrito', CartViewSet, basename='cart')
router.register(r'pedidos', OrderViewSet, basename='order')

urlpatterns = [
    path('checkout/', CheckoutView.as_view({'post': 'checkout'}), name='checkout'),
    path('pago/', PaymentView.as_view({'post': 'process_payment'}), name='process_payment'),
] + router.urls
