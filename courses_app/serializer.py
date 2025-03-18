from rest_framework import serializers
from .models import (
    Course, Group, Table,
    Homework, TableType,
    HomeworkSubmission, HomeworkCheck
)
from users_app.models import Teacher, Student


class CourseSerializer(serializers.ModelSerializer):
    """
    Kurs modeli uchun serializer
    Bu serializer faqat admin tomonidan kurslarni yaratish, o‘zgartirish va o‘chirish uchun ishlatiladi
    """
    class Meta:
        model = Course
        fields = ['id', 'title', 'descriptions']
        read_only_fields = ['id']


class GroupSerializer(serializers.ModelSerializer):
    """
    Guruh modeli uchun serializer
    Guruh ichiga o‘qituvchilar va talabalarni qo‘shish mumkin
    """
    teachers = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), many=True, required=False
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'course', 'teachers', 'created_at']
        read_only_fields = ['id', 'created_at']


class TableTypeSerializer(serializers.ModelSerializer):
    """
    Jadval turi (TableType) modeli uchun serializer
    Bu jadval turini yaratish va boshqarish uchun ishlatiladi
    """
    class Meta:
        model = TableType
        fields = '__all__'
        read_only_fields = ['id']


class TableSerializer(serializers.ModelSerializer):
    """
    Jadval modeli uchun serializer
    Bu model ma’lumotlarni saqlash va boshqarish uchun ishlatiladi
    """
    class Meta:
        model = Table
        fields = '__all__'
        read_only_fields = ['id', 'created_by']


class HomeworkSerializer(serializers.ModelSerializer):
    """
    Uyga vazifa (Homework) modeli uchun serializer
    Faqat o‘qituvchilar uyga vazifa yaratishi mumkin
    """
    class Meta:
        model = Homework
        fields = '__all__'
        read_only_fields = ['id', 'created_by']


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    """
    Uyga vazifalarni topshirish (HomeworkSubmission) modeli uchun serializer
    Faqat talabalar topshirishi mumkin, va ularning kimligi avtomatik belgilanadi
    """
    class Meta:
        model = HomeworkSubmission
        fields = '__all__'
        read_only_fields = ['id', 'student']


class HomeworkCheckSerializer(serializers.ModelSerializer):
    """
    Uyga vazifalarni tekshirish (HomeworkCheck) modeli uchun serializer
    Faqat o‘qituvchilar uyga vazifalarni baholashi mumkin
    """
    class Meta:
        model = HomeworkCheck
        fields = '__all__'
        read_only_fields = ['id', 'checked_by', 'submission']
