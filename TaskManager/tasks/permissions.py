from rest_framework import permissions


class IsAdminForDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user and request.user.is_staff
        return True

