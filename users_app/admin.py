from django.contrib import admin

from users_app.models import User, Teacher, Student, Parents

admin.site.register([User,Teacher,Student,Parents])
