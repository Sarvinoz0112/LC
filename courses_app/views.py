from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .models import (
    Course, Group, Table,
    Homework, HomeworkSubmission, HomeworkCheck, TableType
)
from users_app.models import Teacher, Student
from .serializer  import (
    CourseSerializer, GroupSerializer,
    TableSerializer, HomeworkSerializer,
    HomeworkSubmissionSerializer, HomeworkCheckSerializer, TableTypeSerializer
)
from config_app.permissions import (
    IsAdminOrReadOnly, IsTeacher,
    IsStudent, IsAdmin
)
from config_app.pagination import Pagination


class CourseViewSet(viewsets.ModelViewSet):
    """
    Faqat admin kurs yaratishi, o'zgartirishi, o‘chirish va ko‘rish huquqiga ega
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]


class GroupViewSet(viewsets.ModelViewSet):
    """
    Faqat admin guruh yaratishi, o'zgartirishi va o‘chirish huquqiga ega
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(operation_description="Guruhga o‘qituvchi qo‘shish (faqat admin).")
    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrReadOnly])
    def add_teacher(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        teacher_id = request.data.get('teacher_id')
        if not teacher_id:
            return Response({"error": "teacher_id kiriting, iltimos."}, status=status.HTTP_400_BAD_REQUEST)

        teacher = get_object_or_404(Teacher, id=teacher_id)
        group.teachers.add(teacher)
        return Response({"message": "O‘qituvchi qo‘shildi"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Guruhdan o‘qituvchini o‘chirish (faqat admin).")
    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrReadOnly])
    def remove_teacher(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        teacher_id = request.data.get('teacher_id')
        if not teacher_id:
            return Response({"error": "teacher_id kiriting, iltimos."}, status=status.HTTP_400_BAD_REQUEST)

        teacher = get_object_or_404(Teacher, id=teacher_id)
        group.teachers.remove(teacher)
        return Response({"message": "O‘qituvchi o‘chirildi"}, status=status.HTTP_200_OK)


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAdmin]
    pagination_class = Pagination


class TableTypeViewSet(viewsets.ModelViewSet):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer
    permission_classes = [IsAdmin]
    pagination_class = Pagination


class HomeworkViewSet(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsTeacher]


class HomeworkSubmissionViewSet(viewsets.ModelViewSet):
    queryset = HomeworkSubmission.objects.all()
    serializer_class = HomeworkSubmissionSerializer
    permission_classes = [IsStudent]


class HomeworkCheckViewSet(viewsets.ModelViewSet):
    queryset = HomeworkCheck.objects.all()
    serializer_class = HomeworkCheckSerializer
    permission_classes = [IsTeacher]
