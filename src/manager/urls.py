from . import views
from django.urls import path

urlpatterns = [
    path('agency/<str:pk>/', 
         views.DetailedAgencyView.as_view(), name = 'agency-endpoint'),
    path('agency/', 
         views.ListAgency.as_view(), name = 'agencies-endpoint'),
    path('project/',
         views.ListProjects.as_view(), name = 'projects-endpoint'),
    path('project/<str:agency_name>/<str:pk>/', 
         views.DetailedProjectView.as_view(), name = 'project-endpoint'),
    path('asset/<str:agency_name>/<str:project_name>/',
         views.AssetView.as_view(), name = 'asset-endpoint'),
    path('asset/<str:agency_name>/<str:project_name>/<str:asset_name>/',
         views.AssetViewDetailed.as_view(), name = 'asset-delete-endpoint'),
    path('asset/<str:agency_name>/<str:project_name>/<str:asset_name>/<str:asset_type>/',
         views.GetAssetView.as_view(), name = 'asset-get-endpoint'),
]
