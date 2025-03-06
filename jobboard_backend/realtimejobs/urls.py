from rest_framework.routers import DefaultRouter  # type: ignore
from django.urls import path, include  # type: ignore
from realtimejobs import views

router = DefaultRouter()

router.register(r'jobposts', views.JobpostViewSet, basename='jobpost')


urlpatterns = [
    path('', include(router.urls)),
]
