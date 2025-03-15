from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from .models import Course, Group
from users_app.models import Teacher, Student
from .serializer import CourseSerializer, GroupSerializer
from config_app.permissions import IsAdminOrReadOnly


class CourseViewSet(viewsets.ModelViewSet):
    """
    Faqat admin kurs yaratishi, o'zgartirishi, o‘chirish va ko‘rish huquqiga ega
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]

    @swagger_auto_schema(operation_description="Faqat admin kurs yaratishi mumkin.")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="Faqat admin kursni o‘zgartira oladi.")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Faqat admin kursni o‘chira oladi.")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="Faqat admin kurslarni ko‘ra oladi.")
    def list(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "Faqat admin kurslarni ko‘ra oladi."}, status=status.HTTP_403_FORBIDDEN)
        return super().list(request, *args, **kwargs)


class GroupViewSet(viewsets.ModelViewSet):
    """
    Faqat admin guruh yaratishi, o'zgartirishi va o‘chirish huquqiga ega.
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

    @swagger_auto_schema(operation_description="Guruhga talaba qo‘shish (faqat admin).")
    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrReadOnly])
    def add_student(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        student_id = request.data.get('student_id')
        if not student_id:
            return Response({"error": "student_id kiriting, iltimos."}, status=status.HTTP_400_BAD_REQUEST)

        student = get_object_or_404(Student, id=student_id)
        group.students.add(student)
        return Response({"message": "Talaba qo‘shildi"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_description="Guruhdan talabani o‘chirish (faqat admin).")
    @action(detail=True, methods=['post'], permission_classes=[IsAdminOrReadOnly])
    def remove_student(self, request, pk=None):
        group = get_object_or_404(Group, pk=pk)
        student_id = request.data.get('student_id')
        if not student_id:
            return Response({"error": "student_id kiriting, iltimos."}, status=status.HTTP_400_BAD_REQUEST)

        student = get_object_or_404(Student, id=student_id)
        group.students.remove(student)
        return Response({"message": "Talaba o‘chirildi"}, status=status.HTTP_200_OK)
