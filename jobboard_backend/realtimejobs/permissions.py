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


class IsAdminOrReadCreateOnly(permissions.BasePermission):
    """
    Custom permission:
    - Admins can update and delete.
    - Anyone (authenticated or not) can read.
    - Authenticated users can create.
    """

    def has_permission(self, request, view):
        # Allow GET (read-only) for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow create if authenticated
        if request.method == "POST":
            return request.user and request.user.is_authenticated
        # Allow update/delete only for admins
        return request.user and request.user.is_staff
