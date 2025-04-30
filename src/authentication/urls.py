from . import views
from django.urls import path

app_name = 'authentication'

urlpatterns = [
    path('register/', views.Register.as_view(), name = 'register-endpoint'),
    path('login/', views.Login.as_view(), name = 'login-endpoint'),
    path('logout/', views.Logout.as_view(), name = 'logout-endpoint')
]