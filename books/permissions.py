from rest_framework import permissions


# Permissions 
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow only users to modify their books
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user