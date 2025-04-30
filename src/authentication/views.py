from . import serializers
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated


class Register(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body = serializers.RegisterSerializer)
    def post(self, request):
        serializer = serializers.RegisterSerializer(data = request.data)
        if serializer.is_valid():
            new_user = User.objects.create_user(username = serializer.validated_data.get('username'),
                                                password = serializer.validated_data.get('password'))
            refresh_token = RefreshToken.for_user(user = new_user)
            access_token = str(refresh_token.access_token)

            return Response({
                'message' : 'Successfully registered an account!',
                'access_token' : access_token,
                'refresh_token' : str(refresh_token)
            },
            status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body = serializers.LoginSerializer)
    def post(self, request):
        serializer = serializers.LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.get_user()
            refresh_token = RefreshToken.for_user(user = user)
            access_token = str(refresh_token.access_token)

            return Response({
                'message' : 'Successfully logged in!',
                'access_token' : access_token,
                'refresh_token' : str(refresh_token)
            },
            status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass