from django.shortcuts import render  # type: ignore
from rest_framework import permissions  # type: ignore
from rest_framework import renderers  # type: ignore
from rest_framework import viewsets  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework import viewsets, status, generics  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import AllowAny  # type: ignore
from rest_framework.decorators import action  # type: ignore


from .models import JobPost
from .serializers import JobPostSerializer, RegisterUserSerializer, UserSerializer, ChangePasswordSerializer
from django.contrib.auth import get_user_model  # type: ignore

User = get_user_model()


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


class JobpostViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = (IsAuthenticated, )
