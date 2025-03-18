from django.db import models
from rest_framework.exceptions import PermissionDenied


class Course(models.Model):
    """ Kurslar modeli """
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Group(models.Model):
    """ Talabalar va o‘qituvchilarni birlashtiradigan guruhlar modeli """
    name = models.CharField(max_length=255, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="groups")
    teachers = models.ManyToManyField('users_app.Teacher', related_name="teaching_groups")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class TableType(models.Model):
    """ Jadval turlari modeli (Exam, Lecture, Practice) """
    name = models.CharField(max_length=100, unique=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Table(models.Model):
    """ Ma’lumotlarni saqlash uchun umumiy jadval modeli """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    table_type = models.ForeignKey(TableType, on_delete=models.CASCADE, related_name="tables")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('users_app.User', on_delete=models.CASCADE, related_name="created_tables")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """ Faqat admin foydalanuvchilar jadval yaratishi mumkin """
        if not self.created_by.is_superuser:
            raise PermissionDenied("Faqat admin Table yaratishi mumkin!")
        super().save(*args, **kwargs)


class Homework(models.Model):
    """ O'qituvchilar yaratadigan uy vazifalari modeli """
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name="homeworks")
    created_by = models.ForeignKey('users_app.Teacher', on_delete=models.CASCADE, related_name="created_homeworks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.table.title}"

    def save(self, *args, **kwargs):
        """ Faqat o‘qituvchilar uy vazifasi yaratishi mumkin """
        if not self.created_by.user.groups.filter(name='Teachers').exists():
            raise PermissionDenied("Faqat Teacher Homework yaratishi mumkin!")
        super().save(*args, **kwargs)


class HomeworkSubmission(models.Model):
    """ Talabalar topshiradigan uy vazifalari modeli """
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name="submissions")
    student = models.ForeignKey('users_app.Student', on_delete=models.CASCADE, related_name="submitted_homeworks")
    file = models.FileField(upload_to="homework_submissions/")
    submitted_at = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.homework.title}"

    def save(self, *args, **kwargs):
        """ Faqat talabalar uy vazifasi topshirishi mumkin """
        if not self.student.user.groups.filter(name='Students').exists():
            raise PermissionDenied("Faqat Student homework topshirishi mumkin!")
        super().save(*args, **kwargs)


class HomeworkCheck(models.Model):
    """ O'qituvchilar tomonidan baholanadigan uy vazifalari modeli """
    submission = models.OneToOneField(HomeworkSubmission, on_delete=models.CASCADE, related_name="check_homework")
    checked_by = models.ForeignKey('users_app.Teacher', on_delete=models.CASCADE, related_name="checked_homeworks")
    feedback = models.TextField()
    degree = models.PositiveIntegerField()
    checked_at = models.DateTimeField(auto_now_add=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Checked by {self.checked_by.user.username} - {self.submission.homework.title}"

    def save(self, *args, **kwargs):
        """ Faqat o‘qituvchilar baholashi mumkin """
        if not self.checked_by.user.groups.filter(name='Teachers').exists():
            raise PermissionDenied("Faqat Teacher baholashi mumkin!")
        super().save(*args, **kwargs)
