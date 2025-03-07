from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin  # type: ignore
from django.db import models  # type: ignore
from django.utils.text import slugify  # type: ignore
from django.core.validators import MaxLengthValidator  # type: ignore

import uuid


# Custom User Manager for handling user creation
class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model that provides methods
    to create regular users and superusers.
    """

    def create_user(self, email, full_name, password=None, **extra_fields):
        """
        Creates and returns a regular user.

        :param email: Required. User's unique email.
        :param full_name: Required. User's full name.
        :param password: Optional. If provided, it will be hashed.
        :param extra_fields: Additional fields to set on the user.
        :return: User instance.
        """
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)

        if password:
            user.set_password(password)  # Securely set password
        else:
            user.set_unusable_password()  # Prevent login without password

        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        """
        Creates and returns a superuser.

        :param email: Required. Superuser's unique email.
        :param full_name: Required. Superuser's full name.
        :param password: Required. Password for authentication.
        :param extra_fields: Additional fields to set on the superuser.
        :return: Superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, full_name, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that replaces the default Django user.
    Uses email as the unique identifier instead of a username.
    """

    email = models.EmailField(
        unique=True,
        db_index=True,  # Index added for fast lookups
        help_text="User's unique email address, used for login."
    )
    full_name = models.CharField(
        max_length=255,
        blank=False,
        null=False,
        help_text="User's full name (first and last name)."
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,  # Useful for filtering active users in queries
        help_text="Indicates whether the user account is active."
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether this user can access the admin site."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,  # ✅ Useful for sorting users by registration date
        help_text="Timestamp when the user was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the user was last updated."
    )

    objects = CustomUserManager()  # Attach the custom manager

    # Use email as the unique identifier instead of a username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']  # Required when creating a superuser

    def save(self, *args, **kwargs):
        """
        Custom save method to normalize email and full name.
        """
        self.full_name = self.full_name.title()  # Capitalize full name
        self.email = self.email.lower()  # Store email in lowercase
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the user.
        """
        return f"{self.full_name} ({self.email})"


class Company(models.Model):
    """
    Stores company details for job postings.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)  # Helps with database merging
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        help_text="Company name (must be unique)."
    )
    logo = models.ImageField(
        upload_to='company_logos/',
        null=True,
        blank=True,
        help_text="Company logo image file (optional)."
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Optional company description."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_index=True,  # Index for faster queries when sorting/filtering
        help_text="Timestamp of the last update."
    )
    contact_name = models.CharField(
        max_length=255, null=False, blank=False, help_text="Full name of the contact person.")
    contact_email = models.EmailField(unique=True, db_index=True, null=False,
                                      blank=False, help_text="User email for contact purposes.")

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Tags to categorize job posts (e.g., Python, Remote, Entry-level).
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )  # Unique ID for better scalability

    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,  # Faster tag lookups
        help_text="Tag name for categorizing jobs."
    )

    slug = models.SlugField(
        unique=True,
        db_index=True,  # Improves search and SEO performance
        help_text="SEO-friendly identifier for the tag."
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            # Auto-generate slug from name
            self.slug = slugify(self.name).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class JobType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return self.name


class JobPost(models.Model):
    """
    Stores job postings and links them to a company and relevant tags.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )  # Unique & secure identifier
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='job_posts')
    job_url = models.CharField(
        max_length=2083,  # 2083 is the max URL length in modern browsers
        null=False,
        blank=False,
        db_index=True,  # Now indexing will work
        help_text="Direct URL to the job post."
    )

    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        db_index=True,  # Optimized title search
        help_text="Job title."
    )

    slug = models.SlugField(
        unique=True,
        db_index=True,  # Used for SEO-friendly job URLs
        help_text="SEO-friendly identifier for the job."
    )

    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,  # Improves filtering by location
        help_text="Job location (or NULL if worldwide)."
    )

    is_worldwide = models.BooleanField(
        default=False,
        db_index=True,  # Helps in remote job filtering
        help_text="True if the job is remote."
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name="job_posts",
        null=False,
        blank=False,
        db_index=True,
        help_text="Category of the job post."
    )

    job_type = models.ForeignKey(
        'JobType', on_delete=models.CASCADE, db_index=True)

    salary = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Salary range (e.g., '$100K - $200K')."
    )

    description = models.TextField(
        null=False,
        blank=False,
        help_text="Detailed job description."
    )

    short_description = models.TextField(
        null=False,
        blank=False,
        validators=[MaxLengthValidator(200)],  # Limit to 200 characters
        help_text="Short summary of the job (max 200 characters)."
    )

    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name="job_posts",
        db_index=True,  # Optimized company-job lookup
        help_text="Company offering the job."
    )

    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name="job_posts",
        help_text="Tags associated with this job."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,  # Sorting jobs by newest first
        help_text="Job post creation date."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        db_index=True,  # Tracking updates efficiently
        help_text="Timestamp of the last update."
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Auto-generate slug from title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class JobInteraction(models.Model):
    """
    Tracks user interactions with job posts, including saved jobs and applications.
    """
    STATUS_CHOICES = [
        ('saved', 'Saved'),
        ('applied', 'Applied')
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column="id"
    )  # Ensures unique interaction identification

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,  # Optimized lookup by user
        help_text="User who interacted with the job."
    )

    job = models.ForeignKey(
        'JobPost',
        on_delete=models.CASCADE,
        db_index=True,  # Optimized lookup by job
        help_text="The job post the user interacted with."
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        db_index=True,  # Faster queries for saved/applied statuses
        help_text="Interaction type (saved or applied)."
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,  # Sorting interactions by most recent
        help_text="Time when the interaction occurred."
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'job', 'status'], name='unique_user_job_status')
        ]  # Allows both saved & applied separately
        indexes = [
            # Faster queries for saved/applied jobs per user
            models.Index(fields=['user', 'status']),
            # Optimized lookup for user-job interactions
            models.Index(fields=['user', 'job']),
            # Filtering interactions per job
            models.Index(fields=['job', 'status']),
        ]

    def __str__(self):
        return f"{self.user} - {self.job} ({self.status})"


class JobAlert(models.Model):
    """
    Stores job alerts for users, allowing multiple category and job type preferences.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )  # Unique identifier for job alerts

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,  # Optimize user lookup
        help_text="User who set up the job alert."
    )

    email = models.EmailField(
        db_index=True,
        help_text="User's email for receiving alerts."
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Indicates if the alert is active."
    )

    categories = models.ManyToManyField(
        Category,
        blank=True,
        help_text="Selected job categories for alerts."
    )

    job_types = models.ManyToManyField(
        JobType, blank=True, help_text="Selected job types for alerts.")

    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        help_text="Preferred job location."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when the alert was created."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of the last update."
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'], name='unique_user_job_alert')
            # Ensures a user can only have ONE job alert
        ]
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        return f"Job Alert for {self.user.email} ({'Active' if self.is_active else 'Inactive'})"
