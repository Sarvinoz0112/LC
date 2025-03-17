from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet, GroupViewSet, TableTypeViewSet, TableViewSet,
    HomeworkViewSet, HomeworkSubmissionViewSet, HomeworkCheckViewSet
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'table-types', TableTypeViewSet, basename='table-type')
router.register(r'tables', TableViewSet, basename='table')
router.register(r'homeworks', HomeworkViewSet, basename='homework')
router.register(r'homework-submissions', HomeworkSubmissionViewSet, basename='homework-submission')
router.register(r'homework-checks', HomeworkCheckViewSet, basename='homework-check')

# `app_name` ni qo'shamiz
app_name = 'courses'

urlpatterns = [
    path('', include(router.urls)),
]
