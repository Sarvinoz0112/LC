from django.urls import path, include
from rest_framework.routers import DefaultRouter
from attendance_app.views import AttendanceViewSet

# Router
router = DefaultRouter()
router.register(r'attendances', AttendanceViewSet, basename='attendance')

# `app_name` ni qo'shamiz
app_name = "attendance"

urlpatterns = [
    path('', include(router.urls)),  # Router orqali avtomatik URL generatsiya qilinadi
]
