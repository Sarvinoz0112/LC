from datetime import datetime

from django.db.models import Count, Q
from django.utils.timezone import make_aware
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from config_app.permissions import IsAdmin

from courses_app.models import Course
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

        start_date = make_aware(datetime.combine(start_date, datetime.min.time()))
        end_date = make_aware(datetime.combine(end_date, datetime.max.time()))

        course_statistics = (
            Course.objects.annotate(
                registered_count=Count("c_student", filter=Q(c_student__created_at__range=[start_date, end_date])),
                studying_count=Count("c_student", filter=Q(c_student__group__active=True, c_student__created_at__range=[start_date, end_date])),
                graduated_count=Count("c_student", filter=Q(c_student__group__active=False, c_student__created_at__range=[start_date, end_date])),
                failed_count=Count("c_student", filter=Q(~Q(c_student__group__active=True) & ~Q(c_student__group__active=False), c_student__created_at__range=[start_date, end_date]))
            ).values("title", "registered_count", "studying_count", "graduated_count", "failed_count")
        )

        return Response(course_statistics, status=status.HTTP_200_OK)
