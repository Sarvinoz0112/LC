from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from .models import Payment, PaymentStatus, PaymentMethod, Month
from .serializer import PaymentSerializer, PaymentStatusSerializer, PaymentMethodSerializer, MonthSerializer

class PaymentStatusViewSet(viewsets.ModelViewSet):
    """
    Payment statuslarini boshqarish
    """
    queryset = PaymentStatus.objects.all()
    serializer_class = PaymentStatusSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

class PaymentMethodViewSet(viewsets.ModelViewSet):
    """
    Payment methodlarni boshqarish
    """
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

class MonthViewSet(viewsets.ModelViewSet):
    """
    Oyliklarni boshqarish
    """
    queryset = Month.objects.all()
    serializer_class = MonthSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

class PaymentViewSet(viewsets.ModelViewSet):
    """
    To‘lovlarni boshqarish
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    @swagger_auto_schema(request_body=PaymentSerializer)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(request_body=PaymentSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=PaymentSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
