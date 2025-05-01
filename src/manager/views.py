from . import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, AllowAny

class CreateAgency(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, agency_name: str):
        serializer = serializers.AgencySerializer(data = {'agency_name' : agency_name})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : f'Agency {serializer.validated_data.get('agency_name')} created!'
            },
            status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
class CreateProject(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, agency_name: str, project_name: str):
        pass