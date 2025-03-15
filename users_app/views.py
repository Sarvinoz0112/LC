from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .serializers import *
from config_app.permissions import AdminUser

class UserListView(ListAPIView):
    """
    Foydalanuvchilar ro‘yxatini olish uchun API
    Faqat admin foydalanishi mumkin
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminUser]

class UserDetailView(RetrieveAPIView):
    """
    Berilgan ID bo‘yicha foydalanuvchini olish
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

class UserCreateView(CreateAPIView):
    """
    Yangi foydalanuvchi yaratish
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminUser]

class UserUpdateView(UpdateAPIView):
    """
    Foydalanuvchi ma’lumotlarini yangilash
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

class UserDeleteView(DestroyAPIView):
    """
    Foydalanuvchini o‘chirish
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

class TeacherList(ListAPIView):
    """
    O‘qituvchilar ro‘yxatini olish
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [AdminUser]

class TeacherUpdateView(UpdateAPIView):
    """
    O‘qituvchi ma’lumotlarini yangilash
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

class TeacherRetrieveAPIView(RetrieveAPIView):
    """
    Berilgan ID bo‘yicha o‘qituvchini olish
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'id'
    permission_classes = [AdminUser]

class TeacherCreateAPIView(APIView):
    """
    Yangi o‘qituvchi yaratish
    """
    @swagger_auto_schema(request_body=UserAndTeacherSerializer)
    def post(self, request):
        user_data = request.data.get('user', {})
        user_serializer = UserSerializer(data=user_data)

        if user_serializer.is_valid():
            user = user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        teacher_data = request.data.get('teacher', {})
        teacher_serializer = TeacherSerializer(data=teacher_data)

        if teacher_serializer.is_valid():
            teacher = teacher_serializer.save(user=user)
            return Response(TeacherSerializer(teacher).data, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTeachersByIdsView(APIView):
    """ O‘qituvchilarni ID bo‘yicha olish uchun API """
    def post(self, request):
        serializer = GetTeachersByIdsSerializer(data=request.data)
        if serializer.is_valid():
            teachers = serializer.get_teachers()
            teacher_data = [{"id": teacher.id, "name": teacher.name} for teacher in teachers]
            return Response(teacher_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentApiView(APIView):
    """
    Talabalarni boshqarish uchun API
    """
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__phone', 'user__full_name']

    @swagger_auto_schema(request_body=StudentSerializer)
    def post(self, request):
        """
        Yangi talaba qo‘shish
        """
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'detail': "Talaba yaratildi"}, status=status.HTTP_201_CREATED)
        return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Barcha talabalar ro‘yxatini olish
        """
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetStudentsByIdsView(APIView):
    """ Talabalarni ID bo‘yicha olish uchun API """
    def post(self, request):
        serializer = GetStudentsByIdsSerializer(data=request.data)
        if serializer.is_valid():
            students = serializer.get_students()
            student_data = [{"id": student.id, "name": student.name} for student in students]
            return Response(student_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParentsApiView(APIView):
    """
    Ota-onalarni boshqarish uchun API
    """
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=ParentsSerializer)
    def post(self, request):
        """
        Yangi ota-ona ma’lumotlarini qo‘shish
        """
        serializer = ParentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': True, 'detail': "Ota-ona yaratildi"}, status=status.HTTP_201_CREATED)
        return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        """
        Barcha ota-onalar ro‘yxatini olish
        """
        parents = Parents.objects.all()
        data = [
            {
                'full_name': parent.full_name,
                'phone_number': parent.phone_number,
                'student': parent.student.user.full_name if parent.student else None
            }
            for parent in parents
        ]
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, parent_id):
        """
        Berilgan ID bo‘yicha ota-onani o‘chirish
        """
        parent = get_object_or_404(Parents, id=parent_id)
        parent.delete()
        return Response({'status': True, 'detail': "Ota-ona o‘chirildi"}, status=status.HTTP_204_NO_CONTENT)
