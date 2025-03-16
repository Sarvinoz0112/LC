from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """ Faqat admin foydalanuvchilar ruxsat olishi mumkin """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsTeacher(permissions.BasePermission):
    """ Faqat Teachers guruhidagi foydalanuvchilar ruxsat olishi mumkin """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Teachers').exists()


class IsStudent(permissions.BasePermission):
    """ Faqat Students guruhidagi foydalanuvchilar ruxsat olishi mumkin """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Students').exists()


class IsAdminOrReadOnly(permissions.BasePermission):
    """ Adminlar yaratishi va o‘zgartirishi mumkin, boshqa foydalanuvchilar faqat GET so‘rovini yuborishi mumkin """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_superuser


class AdminOrTeacher(permissions.BasePermission):
    """ Faqat adminlar va o‘qituvchilar attendance qo‘shishi va o‘zgartirishi mumkin """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_superuser or request.user.groups.filter(name='Teachers').exists()
        )