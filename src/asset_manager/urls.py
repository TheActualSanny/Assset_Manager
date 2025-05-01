from django.contrib import admin
from django.urls import path, include

api_endpoint = 'api/v1/{endpoint}'

<<<<<<< Updated upstream
=======
schema = get_schema_view(
    openapi.Info(
        title = 'Asset Manager DOCS',
        default_version = 'v1.0.0',
        description = 'An API which lets client agencies manage their assets.'
    ),
    permission_classes = (AllowAny,)
)

>>>>>>> Stashed changes
urlpatterns = [
    path('admin/', admin.site.urls),
    path(api_endpoint.format(endpoint = 'authentication'), 
         include('authentication.urls', namespace = 'authentication'))
]
