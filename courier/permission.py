from rest_framework import permissions


class IsCourier(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_staff
