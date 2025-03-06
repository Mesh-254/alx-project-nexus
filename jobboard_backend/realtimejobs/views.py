from django.shortcuts import render #type: ignore
from rest_framework import permissions #type: ignore
from rest_framework import renderers #type: ignore
from rest_framework import viewsets #type: ignore
from rest_framework.permissions import IsAuthenticated #type: ignore

from .models import JobPost
from .serializers import JobPostSerializer
 

class JobpostViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    # permission_classes = (IsAuthenticated, )

