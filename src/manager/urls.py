from . import views
from django.urls import path

urlpatterns = [
    path('agency/<str:agency_name>/', 
         views.CreateAgency.as_view(), name = 'agency-endpoint'),
    path('project/<str:agency_name>/<str:project_name>/', 
         views.CreateProject.as_view(), name = 'project-endpoint')
]
