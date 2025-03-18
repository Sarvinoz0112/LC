from datetime import datetime

from django.db.models import Count, Q
from django.utils.timezone import make_aware
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from config_app.permissions import IsAdmin

from users_app.models import Student
from .serializers import DateIntervalSerializer


class StudentStatisticsView(APIView):
    permission_classes = [IsAdmin]

    @swagger_auto_schema(request_body=DateIntervalSerializer)
    def post(self, request):
        serializer = DateIntervalSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        """ Sana va vaqt obyektlarini timezone-aware formatga o'tkazish """
        start_date = make_aware(datetime.combine(start_date, datetime.min.time()))
        end_date = make_aware(datetime.combine(end_date, datetime.max.time()))

        total_students = Student.objects.count()
        """ Bitirgan talabalar soni (faol bo‘lmagan guruhda va sanalar oralig‘ida) """
        graduated_students = Student.objects.filter(group__active=False, created_at__range=[start_date, end_date]).count()
        """ Hozirda o‘qiyotgan talabalar soni (faol guruhda va sanalar oralig‘ida) """
        studying_students = Student.objects.filter(group__active=True, created_at__range=[start_date, end_date]).count()
        """ Belgilangan sanalar oralig‘ida ro‘yxatdan o‘tgan talabalar soni """
        registered_students = Student.objects.filter(created_at__range=[start_date, end_date]).count()

        return Response({
            "total_students": total_students,
            "registered_students": registered_students,
            "studying_students": studying_students,
            "graduated_students": graduated_students,
        }, status=status.HTTP_200_OK)
