from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from courses_app.models import Group
from users_app.models import Teacher, User, Student, Parent


class UserAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","password","full_name","phone")
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Teacher
        fields = ('id','user', 'course', 'descriptions')

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Student
        fields = ('id','user','group', 'course', 'descriptions')

class ParentSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True,read_only=True)

    class Meta:
        model = Parent
        fields = ('id','full_name','address','phone_number','descriptions','students')

class SuperUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'password','full_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_superuser(**validated_data)


class GetStudentsByIdsSerializer(serializers.Serializer):
    student_ids = serializers.ListField(child=serializers.IntegerField())

class GetTeachersByIdsSerializer(serializers.Serializer):
    teacher_ids = serializers.ListField(child=serializers.IntegerField())

class UserAndTeacherSerializer(serializers.Serializer):
    user = UserSerializer()
    teacher = TeacherSerializer()

class UserAndStudentSerializer(serializers.Serializer):
    user = UserSerializer()
    student = StudentSerializer()
