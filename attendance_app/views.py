from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from .models import Attendance
from .serializer import AttendanceSerializer
from config_app.permissions import AdminOrTeacher

class AttendanceViewSet(viewsets.ModelViewSet):
    """ Faqat admin va o‘qituvchilar attendance qo‘shishi va o‘zgartirishi mumkin """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, AdminOrTeacher]

    @swagger_auto_schema(request_body=AttendanceSerializer)
    def create(self, request, *args, **kwargs):
        """ Yangi attendance qo‘shish (faqat admin yoki o‘qituvchi) """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(request_body=AttendanceSerializer)
    def update(self, request, *args, **kwargs):
        """ Attendance ma’lumotini yangilash (faqat admin yoki o‘qituvchi) """
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """ Attendance o‘chirish (faqat admin yoki o‘qituvchi) """
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['patch'], url_path='change-status')
    @swagger_auto_schema(request_body=AttendanceSerializer)
    def change_status(self, request, pk=None):
        """ Attendance statusini o‘zgartirish (faqat admin yoki o‘qituvchi) """
        attendance = get_object_or_404(Attendance, pk=pk)
        serializer = AttendanceSerializer(attendance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
