from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User, Teacher, Student, Parents


class UserSerializer(serializers.ModelSerializer):
    """
    Foydalanuvchilar ma'lumotlarini serializer qilish uchun ishlatiladi
    """

    class Meta:
        model = User
        fields = ("id", "password", "full_name", "phone")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Yangi foydalanuvchi yaratishda parolni xavfsiz qilib saqlash
        """
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class SuperUserSerializer(serializers.ModelSerializer):
    """
    Superuser yaratish uchun serializer
    """

    class Meta:
        model = User
        fields = ("id", "password", "full_name", "phone", "is_staff", "is_superuser")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_staff'] = True
        validated_data['is_superuser'] = True
        return super().create(validated_data)


class TeacherSerializer(serializers.ModelSerializer):
    """
    O‘qituvchi ma'lumotlarini serializer qilish uchun ishlatiladi
    """
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)

    class Meta:
        model = Teacher
        fields = ("id", "user", "full_name", "phone", "course", "created", "updated", "descriptions")


class StudentSerializer(serializers.ModelSerializer):
    """
    Talaba ma'lumotlarini serializer qilish uchun ishlatiladi
    """
    full_name = serializers.CharField(source="user.full_name", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)

    class Meta:
        model = Student
        fields = ("id", "user", "full_name", "phone", "group", "course", "created", "updated", "descriptions")


class ParentsSerializer(serializers.ModelSerializer):
    """
    Talabaning ota-onasi yoki vasiylari haqida ma'lumotlarni serializer qilish uchun ishlatiladi
    """
    student_name = serializers.CharField(source="student.user.full_name", read_only=True)
    student_phone = serializers.CharField(source="student.user.phone", read_only=True)

    class Meta:
        model = Parents
        fields = (
            "id", "full_name", "phone_number", "address", "descriptions", "student", "student_name", "student_phone"
        )


class GetStudentsByIdsSerializer(serializers.Serializer):
    """
    Faqat ID lar orqali talabalarni olish uchun serializer
    """
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )

    def validate_student_ids(self, value):
        if not value:
            raise serializers.ValidationError("student_ids bo‘sh bo‘lishi mumkin emas.")
        return value

    def get_students(self):
        return Student.objects.filter(id__in=self.validated_data['student_ids'])


class GetTeachersByIdsSerializer(serializers.Serializer):
    """
    Faqat ID lar orqali o‘qituvchilarni olish uchun serializer
    """
    teacher_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )

    def validate_teacher_ids(self, value):
        if not value:
            raise serializers.ValidationError("teacher_ids bo‘sh bo‘lishi mumkin emas.")
        return value

    def get_teachers(self):
        return Teacher.objects.filter(id__in=self.validated_data['teacher_ids'])


class UserAndTeacherSerializer(serializers.Serializer):
    """
    Foydalanuvchi va unga bog‘liq o‘qituvchi ma'lumotlarini serializer qilish uchun ishlatiladi
    """
    user = UserSerializer()
    teacher = TeacherSerializer()


class UserAndStudentSerializer(serializers.Serializer):
    """
    Foydalanuvchi va unga bog‘liq talaba ma'lumotlarini serializer qilish uchun ishlatiladi
    """
    user = UserSerializer()
    student = StudentSerializer()
