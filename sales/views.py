from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem, Payment
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, CheckoutSerializer, PaymentSerializer

class CartViewSet(viewsets.ViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().first()

    def list(self, request):
        cart = self.get_object()
        if not cart:
            cart = Cart.objects.create(user=request.user)
        serializer = self.serializer_class(cart)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        return self.list(request)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        cart = self.get_object()
        if not cart:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)

        product_id = request.data.get('product')
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()

        serializer = self.get_serializer(cart)
        return Response(serializer.data)

class CheckoutView(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total=cart.total,
                shipping_cost=10.00,  # Fixed shipping cost, can be calculated based on method
                address=serializer.validated_data['shipping_address']
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart.items.all().delete()  # Clear cart

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data)

class PaymentView(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def process_payment(self, request):
        order_id = request.data.get('order_id')
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        # Simulate payment processing
        payment_status = 'APPROVED' if request.data.get('simulate_success', True) else 'REJECTED'

        payment = Payment.objects.create(
            order=order,
            amount=order.total + order.shipping_cost,
            status=payment_status,
            transaction_id=f"txn_{order.id}"
        )

        if payment_status == 'APPROVED':
            order.status = 'PAID'
            order.save()

        serializer = PaymentSerializer(payment)
        return Response({'status': payment_status, 'payment': serializer.data})

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def comprobante(self, request, pk=None):
        order = self.get_object()
        # In a real implementation, generate PDF here
        return Response({'url': f'/media/comprobantes/order_{order.id}.pdf'})

    @action(detail=True, methods=['get'])
    def estado(self, request, pk=None):
        order = self.get_object()
        return Response({
            'status': order.status,
            'tracking_url': f'https://tracking.example.com/{order.id}' if order.status == 'SHIPPED' else None
        })
