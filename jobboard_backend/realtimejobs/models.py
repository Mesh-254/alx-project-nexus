from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin  # type: ignore
from django.db import models  # type: ignore
from django.utils.text import slugify  # type: ignore
from django.core.validators import MaxLengthValidator  # type: ignore
from django_ckeditor_5.fields import CKEditor5Field  # type: ignore

import uuid

# =============================================================================
# Custom User Manager
# =============================================================================


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
            user.set_password(password)  # Securely set password if provided
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


# =============================================================================
# Custom User Model
# =============================================================================
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that replaces the default Django user.
    Uses email as the unique identifier instead of a username.
    """
    email = models.EmailField(
        unique=True,
        db_index=True,  # Fast lookup for email-based queries
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
        db_index=True,  # Optimize filtering for active users
        help_text="Indicates whether the user account is active."
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether this user can access the admin site."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,  # Useful for sorting users by registration date
        help_text="Timestamp when the user was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the user was last updated."
    )

    objects = CustomUserManager()  # Attach the custom user manager

    # Use email as the unique identifier instead of a username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']  # Required when creating a superuser

    def save(self, *args, **kwargs):
        """
        Custom save method to normalize email and full name.
        """
        self.full_name = self.full_name.title()  # Capitalize full name for consistency
        self.email = self.email.lower()  # Store email in lowercase for uniformity
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the user.
        """
        return f"{self.full_name} ({self.email})"


# =============================================================================
# Company Model
# =============================================================================
class Company(models.Model):
    """
    Stores company details for job postings.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)  # Unique identifier for merging databases
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
    description = CKEditor5Field(config_name='default')
    updated_at = models.DateTimeField(
        auto_now=True,
        db_index=True,  # Speed up queries when sorting or filtering by update time
        help_text="Timestamp of the last update."
    )
    contact_name = models.CharField(
        max_length=255, null=False, blank=False,
        help_text="Full name of the contact person."
    )
    contact_email = models.EmailField(
        unique=True, db_index=True, null=False, blank=False,
        help_text="User email for contact purposes."
    )

    def __str__(self):
        """
        String representation of the company.
        """
        return self.name


# =============================================================================
# Tag Model
# =============================================================================
class Tag(models.Model):
    """
    Tags to categorize job posts (e.g., Python, Remote, Entry-level).
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False  # Unique identifier for scalability
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,  # Faster tag lookups
        help_text="Tag name for categorizing jobs."
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,  # Enhances search and SEO performance
        help_text="SEO-friendly identifier for the tag."
    )

    def save(self, *args, **kwargs):
        """
        Auto-generate slug from name if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the tag.
        """
        return self.name


# =============================================================================
# Category Model
# =============================================================================
class Category(models.Model):
    """
    Stores job categories.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    slug = models.SlugField(unique=True, db_index=True)

    def save(self, *args, **kwargs):
        """
        Auto-generate slug from name if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name).lower()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the category.
        """
        return self.name


# =============================================================================
# JobType Model
# =============================================================================
class JobType(models.Model):
    """
    Represents a type of job (e.g., Full-time, Part-time, Contract).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        """
        Returns the name of the job type.
        """
        return self.name


# =============================================================================
# JobPost Model
# =============================================================================
class JobPost(models.Model):
    """
    Stores job postings and links them to a company, category, job type, and tags.
    """
    JOB_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False  # Unique & secure identifier for the job post
    )
    job_url = models.CharField(
        max_length=2083,
        null=False,
        blank=False,
        db_index=True,
        help_text="Direct URL to the job post."
    )
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
        help_text="Job title."
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="SEO-friendly identifier for the job."
    )
    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        help_text="Job location (or NULL if worldwide)."
    )
    is_worldwide = models.BooleanField(
        default=False,
        db_index=True,
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
        'JobType',
        on_delete=models.CASCADE,
        db_index=True,
        help_text="Type of job (e.g., Full-time, Part-time)."
    )
    salary = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Salary range (e.g., '$100K - $200K')."
    )
    description = CKEditor5Field(config_name='default')
    short_description = models.TextField(
        null=False,
        blank=False,
        validators=[MaxLengthValidator(200)],
        help_text="Short summary of the job (max 200 characters)."
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name="job_posts",
        db_index=True,
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
        db_index=True,
        help_text="Job post creation date."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        db_index=True,
        help_text="Timestamp of the last update."
    )
    status = models.CharField(
        max_length=10,
        choices=JOB_STATUS_CHOICES,
        default='draft',
        help_text="Current status of the job post."
    )

    def save(self, *args, **kwargs):
        """
        Auto-generate slug from title if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the job post.
        """
        return self.title


# =============================================================================
# JobInteraction Model
# =============================================================================
class JobInteraction(models.Model):
    """
    Tracks user interactions with job posts, such as saved jobs and applications.
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
    )  # Unique identifier for each interaction

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        help_text="User who interacted with the job."
    )
    job = models.ForeignKey(
        'JobPost',
        on_delete=models.CASCADE,
        db_index=True,
        help_text="The job post the user interacted with."
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        db_index=True,
        help_text="Type of interaction (saved or applied)."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Time when the interaction occurred."
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'job', 'status'], name='unique_user_job_status'
            )
        ]
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'job']),
            models.Index(fields=['job', 'status']),
        ]

    def __str__(self):
        """
        Returns a string representation of the job interaction.
        """
        return f"{self.user} - {self.job} ({self.status})"


# =============================================================================
# JobAlert Model
# =============================================================================
class JobAlert(models.Model):
    """
    Stores job alerts set by users for specific categories and job types.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )  # Unique identifier for the alert

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        help_text="User who set up the job alert."
    )
    email = models.EmailField(
        db_index=True,
        help_text="Email address to receive job alerts."
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Indicates if the alert is active."
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        help_text="Job categories for which the alert is set."
    )
    job_types = models.ManyToManyField(
        JobType,
        blank=True,
        help_text="Job types for which the alert is set."
    )
    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_index=True,
        help_text="Preferred job location for the alert."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when the alert was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of the last update to the alert."
    )

    class Meta:
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['location']),
        ]

    def __str__(self):
        """
        Returns a string representation of the job alert.
        """
        status = "Active" if self.is_active else "Inactive"
        return f"Job Alert for {self.user.email} ({status})"


# =============================================================================
# Payment Model
# =============================================================================
class Payment(models.Model):
    """
    Stores payment details for job postings.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('declined', 'Declined'),
    ]

    job_post = models.ForeignKey(
        JobPost,
        on_delete=models.CASCADE,
        related_name="payments",
        help_text="The job post associated with this payment."
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=20.00,
        help_text="Payment amount for the job posting."
    )
    currency = models.CharField(
        max_length=10,
        default="USD",
        help_text="Currency of the payment."
    )
    email = models.EmailField(
        help_text="Email address associated with the payment."
    )
    tx_ref = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique transaction reference for the payment."
    )
    payment_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the payment."
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when the payment was made."
    )

    def __str__(self):
        """
        Returns a string representation of the payment.
        """
        return f"Payment for {self.job_post.title} - {self.payment_status}"
