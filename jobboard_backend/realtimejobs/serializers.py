from rest_framework import serializers # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from .models import Company, Tag, Category, JobType, JobPost, JobInteraction, JobAlert

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    Handles serialization and deserialization of User objects,
    ensuring proper validation and transformation of fields.
    """

    class Meta:
        model = User
        fields = [
            "email", "full_name", "is_active", "is_staff", "created_at", "updated_at"
        ]
        # These fields cannot be modified via API
        read_only_fields = ["created_at", "updated_at"]

    def validate_email(self, value):
        """
        Ensures the email is always stored in lowercase to maintain consistency.
        """
        return value.lower()

    def create(self, validated_data):
        """
        Custom user creation logic to ensure password is properly hashed
        before saving the user instance.
        """
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # Hash the password before saving
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Custom update method to handle case formatting and password security.
        """
        instance.full_name = validated_data.get(
            "full_name", instance.full_name).title()
        instance.email = validated_data.get("email", instance.email).lower()

        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)  # Hash the new password

        instance.save()
        return instance


class CompanySerializer(serializers.ModelSerializer):
    """
    Serializer for the Company model.
    Handles serialization of company details used in job postings.
    """

    class Meta:
        model = Company
        fields = ['id', 'name', 'logo', 'description',
                  'updated_at', 'contact_name', 'contact_email']
        # ID and last updated timestamp should not be editable
        read_only_fields = ['id', 'updated_at']


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag model.
    Handles job post categorization based on tags like "Python", "Remote", etc.
    """

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        # Slug is automatically generated from the tag name
        read_only_fields = ['id', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    Handles job categories such as "Software Engineering", "Marketing", etc.
    """

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        # Slug is automatically generated from the category name
        read_only_fields = ['id', 'slug']


class JobTypeSerializer(serializers.ModelSerializer):
    """
    Serializer for the JobType model.
    Represents different types of jobs such as "Full-time", "Part-time", "Freelance".
    """

    class Meta:
        model = JobType
        fields = ['id', 'name']
        read_only_fields = ['id']  # ID should not be editable


class JobPostSerializer(serializers.ModelSerializer):
    """
    Serializer for the JobPost model.
    Handles the creation, update, and retrieval of job postings.
    """

    class Meta:
        model = JobPost
        fields = [
            'id', 'user', 'job_url', 'title', 'slug', 'location', 'is_worldwide',
            'category', 'job_type', 'salary', 'description', 'short_description',
            'company', 'tags', 'created_at', 'updated_at'
        ]
        # These fields should not be editable
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']


class JobInteractionSerializer(serializers.ModelSerializer):
    """
    Serializer for JobInteraction model.

    Handles user interactions with job posts, such as saving or applying for jobs.
    """

    class Meta:
        model = JobInteraction
        fields = ['id', 'user', 'job', 'status', 'timestamp']
        # Prevents manual modification of ID and timestamp
        read_only_fields = ['id', 'timestamp']


class JobAlertSerializer(serializers.ModelSerializer):
    """
    Serializer for JobAlert model.

    Allows users to set up job alerts based on selected categories,
    job types, and location.
    """

    class Meta:
        model = JobAlert
        fields = [
            'id', 'user', 'email', 'is_active', 'categories', 'job_types',
            'location', 'created_at', 'updated_at'
        ]
        # Ensures ID and timestamps remain immutable
        read_only_fields = ['id', 'created_at', 'updated_at']
