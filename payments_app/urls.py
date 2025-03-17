from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PaymentStatusViewSet, PaymentMethodViewSet, MonthViewSet, PaymentViewSet
)

router = DefaultRouter()
router.register(r'payment-status', PaymentStatusViewSet, basename='payment-status')
router.register(r'payment-method', PaymentMethodViewSet, basename='payment-method')
router.register(r'month', MonthViewSet, basename='month')
router.register(r'payment', PaymentViewSet, basename='payment')

# `app_name` ni qo'shamiz
app_name = 'payments'

urlpatterns = [
    path('', include(router.urls)),
]
