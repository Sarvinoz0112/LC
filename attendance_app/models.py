from django.db import models

STATUS_CHOICES = [
    ('present', "Bor"),
    ('absent', "Yo‘q"),
    ('late', "Kechikdi"),
]

class Attendance(models.Model):
    group = models.ForeignKey('courses_app.Group', on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey('users_app.Student', on_delete=models.CASCADE, related_name="attendances")
    teacher = models.ForeignKey('users_app.Teacher', on_delete=models.CASCADE, related_name="given_attendances")
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')

    def __str__(self):
        return f"{self.student.username} - {self.group.title} ({self.status})"
