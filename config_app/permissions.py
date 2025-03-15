from rest_framework import permissions
from rest_framework.permissions import BasePermission

class AdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin or request.user.is_staff

class StudentUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_student


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Faqat adminlar kurs yaratishi, o‘zgartirishi va o‘chira olishi mumkin
    Oddiy foydalanuvchilar faqat ko‘rish (GET) huquqiga ega
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff