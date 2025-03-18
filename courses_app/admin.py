from django.contrib import admin

from courses_app.models import Course, Group, TableType, Table, Homework, HomeworkSubmission, HomeworkCheck

admin.site.register([Course, Group, TableType, Table, Homework, HomeworkSubmission, HomeworkCheck])
