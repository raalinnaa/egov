from rest_framework import permissions


class IsActiveUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active is True


class IsNonActiveUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active is False


class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user, request.user.is_staff, request.user.is_superuser)
        return request.user.is_staff is True and not request.user.is_superuser
