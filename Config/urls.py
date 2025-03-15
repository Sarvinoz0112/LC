from django.urls import re_path, path, include
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from users_app.views import (
    UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView,
    TeacherList, TeacherUpdateView, TeacherRetrieveAPIView, TeacherCreateAPIView,
    StudentApiView, ParentsApiView, GetStudentsByIdsView, GetTeachersByIdsView
)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/create/', UserCreateView.as_view(), name='user-create'),
    path('api/users/update/<int:id>/', UserUpdateView.as_view(), name='user-update'),
    path('api/users/delete/<int:id>/', UserDeleteView.as_view(), name='user-delete'),

    path('api/teachers/', TeacherList.as_view(), name='teacher-list'),
    path('api/teachers/<int:id>/', TeacherRetrieveAPIView.as_view(), name='teacher-detail'),
    path('api/teachers/update/<int:id>/', TeacherUpdateView.as_view(), name='teacher-update'),
    path('api/teachers/create/', TeacherCreateAPIView.as_view(), name='teacher-create'),
    path('get-teachers/', GetTeachersByIdsView.as_view(), name='get_teachers'),

    path('api/students/', StudentApiView.as_view(), name='student-list'),
    path('api/students/<int:student_id>/', StudentApiView.as_view(), name='student-detail'),
    path('get-students/', GetStudentsByIdsView.as_view(), name='get_students'),

    path('api/parents/', ParentsApiView.as_view(), name='parents-list'),
    path('api/parents/<int:parent_id>/', ParentsApiView.as_view(), name='parents-detail'),
]
