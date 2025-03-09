from rest_framework import serializers  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from django.contrib.auth.password_validation import validate_password  # type: ignore
from .models import Company, Tag, Category, JobType, JobPost, JobInteraction, JobAlert,  User

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. Handles creating a new user
    while ensuring password hashing and validation.
    """
    password = serializers.CharField(
        write_only=True, required=True, min_length=6,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True, required=True, min_length=6,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password', 'confirm_password']

    def validate(self, data):
        """
        Ensure that password and confirm_password match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        """
        Custom method to create a user with hashed password.
        """
        validated_data.pop(
            'confirm_password')  # Remove confirm_password before saving
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for retrieving and updating user profile.
    """
    url = serializers.HyperlinkedIdentityField(view_name="profile-detail")
    job_posts = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="jobpost-detail"
    )
    password = serializers.CharField(
        write_only=True, required=False, min_length=6,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ["url", "email", "full_name", "password",
                  "is_active", "is_staff", "created_at", "updated_at", "job_posts"]
        read_only_fields = ["email", "is_active",
                            "is_staff", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        """
        Allow users to update profile details.
        """
        instance.full_name = validated_data.get(
            "full_name", instance.full_name)
        # instance.email = validated_data.get("email", instance.email)

        # Hash password if provided
        password = validated_data.get("password")
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    """
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_new_password(self, value):
        """
        Validate the new password strength.
        """
        validate_password(value)
        return value

    def validate(self, data):
        """
        Ensure old password is correct before setting a new one.
        """
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError(
                {"old_password": "Old password is incorrect."})
        return data

    def save(self, **kwargs):
        """
        Set the new password.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Company model.
    Handles serialization of company details used in job postings.
    """
    url = serializers.HyperlinkedIdentityField(view_name="company-detail")

    class Meta:
        model = Company
        fields = ['url', 'id', 'name', 'logo', 'description',
                  'updated_at', 'contact_name', 'contact_email']
        # ID and last updated timestamp should not be editable
        read_only_fields = ['id', 'updated_at']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Tag model.
    Handles job post categorization based on tags like "Python", "Remote", etc.
    """

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        # Slug is automatically generated from the tag name
        read_only_fields = ['id', 'slug']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the Category model.
    Handles job categories such as "Software Engineering", "Marketing", etc.
    """
    url = serializers.HyperlinkedIdentityField(view_name="category-detail")
    job_posts = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="jobpost-detail"
    )

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'slug', 'job_posts']
        # Slug is automatically generated from the category name
        read_only_fields = ['id', 'slug']


class JobTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the JobType model.
    Represents different types of jobs such as "Full-time", "Part-time", "Freelance".
    """
    url = serializers.HyperlinkedIdentityField(view_name="jobtype-detail")

    class Meta:
        model = JobType
        fields = ['url', 'id', 'name']
        read_only_fields = ['id']  # ID should not be editable


class JobPostSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the JobPost model.
    Handles the creation, update, and retrieval of job postings.
    """
    url = serializers.HyperlinkedIdentityField(view_name="jobpost-detail")
    user = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(), view_name="profile-detail"
    )
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(), view_name="category-detail"
    )
    job_type = serializers.HyperlinkedRelatedField(
        queryset=JobType.objects.all(), view_name="jobtype-detail"
    )
    company = serializers.HyperlinkedRelatedField(
        queryset=Company.objects.all(), view_name="company-detail"
    )

    class Meta:
        model = JobPost
        fields = [
            'url', 'id', 'user', 'job_url', 'title', 'slug', 'location', 'is_worldwide',
            'category', 'job_type', 'salary', 'description', 'short_description',
            'company', 'tags', 'created_at', 'updated_at', 'status'
        ]
        # These fields should not be editable
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class JobInteractionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for JobInteraction model.

    Handles user interactions with job posts, such as saving or applying for jobs.
    """

    url = serializers.HyperlinkedIdentityField(view_name="jobinteraction-detail")
    user = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="profile-detail"
    )
    job = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="jobpost-detail"
    )

    class Meta:
        model = JobInteraction
        fields = ['url', 'id', 'user', 'job', 'status', 'timestamp']
        # Prevents manual modification of ID and timestamp
        read_only_fields = ['id', 'timestamp']


class JobAlertSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for JobAlert model.

    Allows users to set up job alerts based on selected categories,
    job types, and location.
    """
    url = serializers.HyperlinkedIdentityField(view_name="jobalert-detail")
    user = serializers.HyperlinkedRelatedField(
        read_only=True, view_name="profile-detail"
    )
    categories = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="category-detail"
    )
    job_types = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="jobtype-detail"
    )

    class Meta:
        model = JobAlert
        fields = [
            'url', 'id', 'user', 'email', 'is_active', 'categories', 'job_types',
            'location', 'created_at', 'updated_at'
        ]
        # Ensures ID and timestamps remain immutable
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
