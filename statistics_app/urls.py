from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentStatisticsView

router = DefaultRouter()

# `app_name` ni qo'shamiz
app_name = "statistics"

urlpatterns = [
    path("", include(router.urls)),
    path("students/statistics/", StudentStatisticsView.as_view(), name="student-statistics"),
]
