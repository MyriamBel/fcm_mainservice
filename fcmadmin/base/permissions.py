from rest_framework import permissions


class IsSuperuser(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_superuser is True


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
