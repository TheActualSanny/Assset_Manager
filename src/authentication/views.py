from . import serializers
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        pass

class Login(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        pass

class Logout(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        pass