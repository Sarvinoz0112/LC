from rest_framework import serializers
from .models import PaymentStatus, PaymentMethod, Month, Payment

# PaymentStatus uchun serializer
class PaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = '__all__'

# PaymentMethod uchun serializer
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

# Month uchun serializer
class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month
        fields = '__all__'

# Payment uchun serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
