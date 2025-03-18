from django.contrib import admin

from users_app.models import User, Teacher, Student, Parent

admin.site.register([User,Teacher,Student,Parent])
