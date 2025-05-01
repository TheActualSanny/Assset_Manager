from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

api_endpoint = 'api/v1/{endpoint}'


schema = get_schema_view(
    openapi.Info(
        title = 'Asset Manager DOCS',
        default_version = 'v1.0.0',
        description = 'An API which lets client agencies manage their assets.'
    ),
    permission_classes = (AllowAny,)
)

urlpatterns = [
    path('', schema.with_ui(), name = 'swagger-docs'),
    path('admin/', admin.site.urls),
    path(api_endpoint.format(endpoint = 'authentication/'), 
         include('authentication.urls', namespace = 'authentication'))
]
