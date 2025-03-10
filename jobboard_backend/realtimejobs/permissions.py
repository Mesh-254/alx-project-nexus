from rest_framework import permissions  # type: ignore


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to manage categories.
    """

    def has_permission(self, request, view):
        # Allow GET (read) requests for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Restrict modification actions to admins only
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed for staff users
        return request.user.is_authenticated and request.user.is_staff


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
            return True
        # Allow update/delete only for admins
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Only admins can update or delete
        return request.user and request.user.is_staff


class IsAdminOnly(permissions.BasePermission):
    """
    Custom permission to allow only admin users to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
