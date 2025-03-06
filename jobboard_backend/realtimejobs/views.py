from django.shortcuts import render  # type: ignore
from rest_framework import permissions  # type: ignore
from rest_framework import renderers  # type: ignore
from rest_framework import viewsets  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework import viewsets, status, generics  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import AllowAny  # type: ignore
from rest_framework.decorators import action  # type: ignore
from django.utils.text import slugify  # type: ignore

# Import raw SQL queries
from realtimejobs.queries.category_queries import CategoryQueries
from .models import JobPost, Category, User, JobType
from .serializers import JobPostSerializer, RegisterUserSerializer, JobTypeSerializer, UserSerializer, ChangePasswordSerializer, CategorySerializer
from django.contrib.auth import get_user_model  # type: ignore
from .permissions import IsAdminOrReadOnly

User = get_user_model()

# ****************USER  VIEWS ************************


class RegisterViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for user registration. Allows new users to create an account.
    """
    serializer_class = RegisterUserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Handles user registration (POST request).
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "User registered successfully!", "user": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for authenticated users to:
    - View their profile (GET /profile/)
    - Update details (PATCH /profile/)
    - Change password (PATCH /profile/change-password/)
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Restrict access to only the authenticated user's profile."""
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        """Ensure the user can only access their own profile."""
        return self.request.user  # This allows updating only the logged-in user

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated], url_path="update-profile")
    def update_profile(self, request):
        """Allow authenticated users to update their profile."""
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated], url_path="change-password")
    def change_password(self, request, pk=None):
        """
        Custom action for changing user password (PATCH /profile/change-password/)
        """
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ****************CATEGORIES VIEW************************

class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides CRUD operations for job categories.
    Uses Django ORM for standard operations.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        """Create a new category (Admin Only)."""
        if not request.user.is_staff:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        name = request.data.get("name")
        if not name:
            return Response({"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)

        slug = slugify(name).lower()

        # Use Django ORM to create the category
        category = Category.objects.create(name=name, slug=slug)

        return Response(
            {"message": "Category created successfully",
                "category": CategorySerializer(category).data},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        """Update an existing category (Admin Only)."""
        if not request.user.is_staff:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        category_id = kwargs.get("pk")

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        # Keep old name if not provided
        name = request.data.get("name", category.name)
        category.name = name
        category.slug = slugify(name).lower()
        category.save()  # Save changes using ORM

        return Response(
            {"message": "Category updated successfully",
                "category": CategorySerializer(category).data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        """Delete a category (Admin Only)."""
        if not request.user.is_staff:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        category_id = kwargs.get("pk")

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        category.delete()  # ORM delete
        return Response({"message": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class JobTypeViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides CRUD operations for job types.
    """
    queryset = JobType.objects.all().order_by("name")  # Optimized query
    serializer_class = JobTypeSerializer
    permission_classes = [IsAdminOrReadOnly]  # Restrict to admin users

    def perform_create(self, serializer):
        """Customize the creation process if needed."""
        serializer.save()

    def perform_update(self, serializer):
        """Customize the update process if needed."""
        serializer.save()

    def perform_destroy(self, instance):
        """Customize the deletion process if needed."""
        instance.delete()



class JobpostViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = (IsAuthenticated, )
