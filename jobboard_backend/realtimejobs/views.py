from django.shortcuts import get_object_or_404, render  # type: ignore
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
from realtimejobs.queries.jobinteraction_queries import JobInteractionQueries
from .models import JobPost, Category, User, JobType, Tag, Company, JobInteraction
from .serializers import *
from django.contrib.auth import get_user_model  # type: ignore
from .permissions import IsAdminOrReadOnly, IsAdminOrReadCreateOnly
from .tasks import send_subscription_email



# **************** USER  VIEWS ************************

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


# **************** CATEGORIES VIEW ************************

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


# ****************JOB TYPE VIEW************************


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


# **************** TAGS VIEW ***********************


class TagsViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides CRUD operations for tags.
    """
    queryset = Tag.objects.all().order_by("name")  # Optimized query
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly]  # Restrict to admin users

    def perform_create(self, serializer):
        """Customize the creation process if needed."""
        serializer.save(slug=slugify(serializer.validated_data["name"]))

    def perform_update(self, serializer):
        """Ensure slug updates when name changes."""
        instance = serializer.instance  # Get the existing object
        name = serializer.validated_data.get("name", instance.name)

        # Update slug only if the name changes
        if name != instance.name:
            serializer.save(slug=slugify(name))
        else:
            serializer.save()


# **************** COMPANY  VIEW ************************


class CompanyViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Company model:
    - Allows anyone to read (GET).
    - Allows authenticated users to create (POST).
    - Allows only admins to update or delete (PUT, PATCH, DELETE).
    """
    queryset = Company.objects.all().order_by("name")
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadCreateOnly]  # Apply custom permission

    def perform_create(self, serializer):
        """Ensures the company is saved correctly when a user creates it."""
        serializer.save()


# ****************JOB INTERACTION  VIEW ***********************


class JobInteractionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling job interactions (saving and applying).
    """
    queryset = JobInteraction.objects.all()
    serializer_class = JobInteractionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Restrict data to the logged-in user."""
        return JobInteraction.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Save a job post as either 'saved' or 'applied'. 
        Ensures a user can save a job under both statuses but only once per status.
        """
        user = request.user
        job_id = request.data.get("job")
        job_status = request.data.get("status")

        # Validate job existence
        job = get_object_or_404(JobPost, id=job_id)

        # Ensure valid job status
        if job_status not in ['saved', 'applied']:
            return Response({"error": "Invalid status. Must be 'saved' or 'applied'."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the interaction already exists
        existing_interaction = JobInteraction.objects.filter(
            user=user, job=job, status=job_status).first()

        if existing_interaction:
            return Response({"message": f"You have already {job_status} this job."}, status=status.HTTP_200_OK)

        # Create job interaction if it doesn't exist
        JobInteraction.objects.create(user=user, job=job, status=job_status)

        return Response({"message": f"Job {job_status} successfully!"}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def saved_jobs(self, request):
        """
        Fetch jobs saved by the logged-in user.
        """
        saved_jobs = JobInteraction.objects.filter(
            user=request.user, status='saved').select_related('job')
        serializer = JobInteractionSerializer(saved_jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def applied_jobs(self, request):
        """
        Fetch jobs applied by the logged-in user.
        """
        applied_jobs = JobInteraction.objects.filter(
            user=request.user, status='applied').select_related('job')
        serializer = JobInteractionSerializer(applied_jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def remove_interaction(self, request, pk=None):
        """
        Remove a saved/applied status for a job.
        """
        user = request.user
        # Renamed from 'status' to 'job_status'
        job_status = request.query_params.get("status")

        if not job_status:
            return Response({"error": "job_status query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        deleted, _ = JobInteraction.objects.filter(
            user=user, job_id=pk, status=job_status).delete()

        if deleted:
            return Response({"message": "Interaction removed successfully."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Interaction not found."}, status=status.HTTP_404_NOT_FOUND)




# ****************JOB ALERT  VIEW************************


class JobAlertViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing job alerts.
    Users can create, update, and delete job alerts.
    """
    queryset = JobAlert.objects.all()
    serializer_class = JobAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Ensure users only see their job alerts."""
        return JobAlert.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Assign the authenticated user to the job alert."""
        job_alert = serializer.save(user=self.request.user)

        # Celery task to send confirmation email
        send_subscription_email.delay(job_alert.id)




class JobpostViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
