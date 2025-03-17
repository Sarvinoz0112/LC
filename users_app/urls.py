from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users_app.views import UserViewSet, TeacherViewSet, StudentViewSet, ParentsViewSet, CreateSuperAdminView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'parents', ParentsViewSet, basename='parent')

# `app_name` ni qo'shamiz
app_name = "users"

urlpatterns = [
    path('', include(router.urls)),  # Router orqali avtomatik URL generatsiya qilinadi
    path('create-superadmin/', CreateSuperAdminView.as_view(), name='create-superadmin'),
]
