from rest_framework import permissions


class IsOwnUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj == request.user


class IsNotAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not request.user.is_authenticated
