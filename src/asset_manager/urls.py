from django.contrib import admin
from django.urls import path, include

api_endpoint = 'api/v1/{endpoint}'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(api_endpoint.format(endpoint = 'authentication'), 
         include('authentication.urls', namespace = 'authentication'))
]
