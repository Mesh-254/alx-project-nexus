from rest_framework import permissions  # type: ignore


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to manage categories.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Restrict modification actions to admins only
        return request.user and request.user.is_staff
