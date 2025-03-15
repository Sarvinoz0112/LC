from rest_framework import serializers
from .models import Course, Group
from users_app.models import Teacher, Student

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'descriptions']

class GroupSerializer(serializers.ModelSerializer):
    teachers = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), many=True, required=False
    )
    students = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), many=True, required=False
    )

    class Meta:
        model = Group
        fields = ['id', 'name', 'course', 'teachers', 'students', 'created_at']
        read_only_fields = ['created_at']
