from . import views
from django.urls import path

urlpatterns = [
    path('agency/<str:agency_name>/', views.CreateAgency.as_view(), name = 'agency-endpoint')
]
