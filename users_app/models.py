from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from courses_app.models import Course


class UserManager(BaseUserManager):
    """
    Foydalanuvchilarni yaratish uchun maxsus manager
    """

    def create_user(self, phone, password=None, **extra_fields):
        """
        Oddiy foydalanuvchi yaratish
        """
        if not phone:
            raise ValueError('Telefon raqami kiritilishi shart')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        """
        Tizimda to‘liq huquqli superuser yaratish
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is_staff=True bo‘lishi kerak.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser is_superuser=True bo‘lishi kerak.')

        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Tizim foydalanuvchilari uchun model
    """
    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon raqami '+998901234567' formatida bo‘lishi kerak."
    )
    phone = models.CharField(validators=[phone_regex], max_length=13, unique=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    username = None

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.full_name if self.full_name else self.phone

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Teacher(models.Model):
    """
    O‘qituvchilar haqida ma’lumot saqlovchi model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ManyToManyField("courses_app.Course", related_name="teachers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.phone


class Student(models.Model):
    """
    Talabalar haqida ma’lumot saqlovchi model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ManyToManyField("courses_app.Group", related_name="group_students")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_students", null=True,
                               blank=True)
    is_line = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.phone


class Parent(models.Model):
    """
    Talabaning ota-onasi yoki vasiylari haqida ma’lumot saqlovchi model
    """
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
