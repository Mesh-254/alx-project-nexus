from rest_framework import permissions  # type: ignore
from drf_yasg.views import get_schema_view  # type: ignore
from drf_yasg import openapi  # type: ignore
from rest_framework.authentication import SessionAuthentication, TokenAuthentication # type: ignore


schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
    authentication_classes=[SessionAuthentication, TokenAuthentication],
    permission_classes=(permissions.AllowAny,),
)
