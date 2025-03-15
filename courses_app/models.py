from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="groups")
    teachers = models.ManyToManyField("users_app.Teacher", related_name="teaching_groups")
    students = models.ManyToManyField("users_app.Student", related_name="student_groups")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
