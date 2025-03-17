from rest_framework import serializers
from rest_framework.fields import DateField
from config_app.permissions import IsAdmin


class DateIntervalSerializer(serializers.Serializer):
    """
    Bu serializer faqat admin foydalanuvchilar uchun sanalar oralig'ini kiritish imkonini beradi
    API orqali statistik ma'lumotlarni olish uchun ishlatiladi
    """

    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    def validate(self, data):
        """
        Faqat admin foydalanuvchilarga sanalar oralig'ini kiritishga ruxsat
        """
        request = self.context.get("request")
        if request and not IsAdmin().has_permission(request, None):
            raise serializers.ValidationError("Sanalar oralig'ini faqat admin foydalanuvchilar kiritishi mumkin.")
        return data
