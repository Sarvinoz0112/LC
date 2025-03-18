from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework.routers import DefaultRouter
from .serializers import *
from .models import User, Teacher, Student, Parent
from config_app.permissions import IsAdmin

'''
Ushbu modul foydalanuvchilar, o‘qituvchilar, talabalar va ota-onalar uchun API-larni taqdim etadi.
Shuningdek, super administrator yaratish funksiyasini ham o‘z ichiga oladi.
'''

# Umumiy User API
class UserViewSet(ModelViewSet):
    '''Foydalanuvchilarni boshqarish uchun API'''
    queryset = User.objects.all()
    serializer_class = UserAllSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'id'

# Teacher API
class TeacherViewSet(ModelViewSet):
    '''O‘qituvchilarni boshqarish uchun API'''
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'id'

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(request_body=UserAndTeacherSerializer)
    def create_teacher(self, request):
        """Yangi o‘qituvchi yaratish"""
        user_data = request.data.get('user', {})
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(is_teacher=True)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        teacher_data = request.data.get('teacher', {})
        teacher_serializer = TeacherSerializer(data=teacher_data)

        if teacher_serializer.is_valid():
            teacher_serializer.save(user=user)
            return Response(teacher_serializer.data, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Student API
class StudentViewSet(ModelViewSet):
    '''Talabalarni boshqarish uchun API'''
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'id'

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(request_body=UserAndStudentSerializer)
    def create_student(self, request):
        """Yangi talaba yaratish"""
        user_data = request.data.get('user', {})
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save(is_student=True)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        student_data = request.data.get('student', {})
        student_serializer = StudentSerializer(data=student_data)
        if student_serializer.is_valid():
            student = student_serializer.save(user=user)
            return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Ota-onalar uchun API
class ParentsViewSet(ModelViewSet):
    '''Ota-onalarni boshqarish uchun API'''
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'id'

# Super Admin yaratish
class CreateSuperAdminView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def post(self, request):
        """SuperAdmin yaratish"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(is_staff=True, is_superuser=True)
            return Response({'status': True, 'detail': "SuperAdmin yaratildi"}, status=status.HTTP_201_CREATED)
        return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Router orqali endpointlarni avtomatik yaratish
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'parents', ParentsViewSet, basename='parent')
