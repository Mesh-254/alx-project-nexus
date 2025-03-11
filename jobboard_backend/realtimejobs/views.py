from django.shortcuts import get_object_or_404, redirect, render  # type: ignore
from django.conf import settings  # type: ignore
from rest_framework import permissions  # type: ignore
from rest_framework import renderers  # type: ignore
from rest_framework import viewsets  # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework import viewsets, status, generics  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.permissions import AllowAny  # type: ignore
from rest_framework.decorators import action  # type: ignore
from django.utils.text import slugify  # type: ignore
from django.http import HttpResponse  # type: ignore
from django.views.decorators.csrf import csrf_exempt  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework.decorators import api_view, permission_classes  # type: ignore
import requests
import uuid
from .models import JobPost, Payment
from realtimejobs.queries.jobpost_queries import JobPostQueries  # type: ignore


# Import raw SQL queries
from realtimejobs.queries.jobinteraction_queries import JobInteractionQueries
from .models import JobPost, Category, User, JobType, Tag, Company, JobInteraction
from .serializers import *
from django.contrib.auth import get_user_model  # type: ignore
from .permissions import IsAdminOrReadOnly, IsAdminOrReadCreateOnly, IsAdminOnly
from .tasks import send_subscription_email, process_successful_payment


# **************** USER  VIEWS ************************

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    """
    Returns the details of the currently logged-in user.
    """
    serializer = UserSerializer(request.user, context={"request": request})
    return Response(serializer.data)


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
        job_alert = serializer.save(user=self.request.user, is_active=True)

        # Celery task to send confirmation email
        send_subscription_email.delay(job_alert.id)


@csrf_exempt
def unsubscribe(request, alert_id):
    if request.method != "POST":
        return HttpResponse({"error": "Invalid request method. Use POST."}, status=405)

    # Get the specific JobAlert instance
    alert = get_object_or_404(JobAlert, id=alert_id)

    # Get the user associated with alert
    user = alert.user

    # Deactivate ALL job alerts for this user
    # alerts = JobAlert.objects.filter(user=user, is_active=True)

    # Delete all job alerts for this user
    JobAlert.objects.filter(user=user).delete()

    # if not alerts.exists():
    #     return HttpResponse("You have already unsubscribed from job alerts.")

    # alerts.update(is_active=False)  # Bulk update to deactivate all alerts

    # alerts = JobAlert.objects.filter(user=user, is_active=False)
    # if alerts:
    #     # Delete all job alerts for this user
    #     alerts.delete()

    return HttpResponse("You have successfully unsubscribed from all job alerts.")


# ****************JOB POST  VIEW ***********************

class JobpostViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAdminOrReadCreateOnly]

    def create(self, request, *args, **kwargs):
        """Handles job creation and payment initiation."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Generate a unique transaction reference
        tx_ref = uuid.uuid4().hex

        # Payment data to be sent to Chapa
        payload = {
            "amount": "20.00",  # Static fee for posting a job
            "currency": "USD",
            "email": job_post.company.contact_email,  # Assuming user email exists
            "tx_ref": tx_ref,
            "callback_url": settings.CHAPA_CALLBACK_URL,  # User is redirected after payment
            "customization": {
                "title": "Job Post Payment",
                "description": "Get your job posted on RealtimeJobs"
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'
        }

        # Send request to Chapa API
        response = requests.post(
            "https://api.chapa.co/v1/transaction/initialize", json=payload, headers=headers)
        data = response.json()

        print(f'payment details {data}')

        # Check if payment initialization was successful
        if data.get('status') == 'success':
            checkout_url = data.get('data', {}).get('checkout_url')
            if not checkout_url:
                return Response({'error': 'Payment initialization failed'}, status=status.HTTP_400_BAD_REQUEST)

            # Save the JobPost using the serializer
            job_post = serializer.save(status='draft')

            # Save payment details
            payment = Payment.objects.create(
                job_post=job_post,
                amount=payload['amount'],
                currency=payload['currency'],
                email=payload['email'],
                tx_ref=payload['tx_ref'],
                payment_status='pending'
            )
            payment.save()

            # Return the checkout URL to redirect the user
            return Response({"checkout_url": checkout_url}, status=status.HTTP_201_CREATED)

        else:
            return Response({'error': 'Payment initialization failed'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentVerificationView(APIView):
    """
    Handles Chapa payment verification.
    If payment is successful, updates job status to "published".
    """

    def get(self, request):
        tx_ref = request.GET.get('tx_ref')

        if not tx_ref:
            return Response({"error": "Transaction reference missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.get(tx_ref=tx_ref)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        # Verify payment using Chapa API
        url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"
        headers = {'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}'}
        response = requests.get(url, headers=headers)
        verification_data = response.json()

        if verification_data.get('status') == 'success':
            # Update payment and job post status
            payment.payment_status = 'success'
            payment.save()

            job_post = payment.job_post
            job_post.status = 'published'
            job_post.save()

            # Redirect frontend users to success page
            frontend_success_url = f"http://localhost:5173/payment-success?tx_ref={tx_ref}"
            return redirect(frontend_success_url)

        return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)


class JobPostListViewSet(viewsets.ViewSet):
    """ViewSet for fetching job posts with multiple filters."""

    def list(self, request):
        """Handle GET requests with multiple filters and pagination."""
        categories = request.GET.getlist(
            "category[]")  # Example: ?category[]=1&category[]=2
        # Example: ?location[]=New York&location[]=Berlin
        locations = request.GET.getlist("location[]")
        # Example: ?job_type[]=1&job_type[]=2
        job_types = request.GET.getlist("job_type[]")
        page = int(request.GET.get("page", 1))
        page_size = int(request.GET.get("page_size", 15))

        job_query = JobPostQueries()
        jobs = job_query.fetch_filtered_jobs(
            categories, locations, job_types, page, page_size)

        return Response({"jobs": jobs, "has_next": len(jobs) == page_size})


class PaymentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing payment instances.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated, IsAdminOnly]
