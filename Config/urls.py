from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="LMS API",
        default_version='v1',
        description="LMS project API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="NematovWork@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include(('users_app.urls', 'users'), namespace='users')),
    path('api/v1/courses/', include(('courses_app.urls', 'courses'), namespace='courses')),
    path('api/v1/attendances/', include(('attendance_app.urls', 'attendance'), namespace='attendances')),
    path('api/v1/auth/', include(('auth_app.urls', 'auth'), namespace='auth')),
    path('api/v1/payments/', include(('payments_app.urls', 'payments'), namespace='payments')),
    path('api/v1/statistics/', include(('statistics_app.urls', 'statistics'), namespace='statistics')),

    # Swagger URL-larini to‘g‘ri yozamiz
    path('swagger.<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
