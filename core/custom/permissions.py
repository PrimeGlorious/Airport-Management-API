from rest_framework import permissions


class IsAdminOrIsAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        else:
            return request.user and request.user.is_staff
