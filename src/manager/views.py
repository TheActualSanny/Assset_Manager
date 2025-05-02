from . import serializers
from rest_framework import status
from .models import Project, Agency
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import DestroyModelMixin, ListModelMixin

class ListAgency(GenericAPIView, ListModelMixin):
    queryset = Agency.objects.all()
    serializer_class = serializers.AgencySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class DetailedAgencyView(GenericAPIView, DestroyModelMixin):
    queryset = Agency.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, agency_name: str):
        serializer = serializers.AgencySerializer(data = {'agency_name' : agency_name})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : f'Agency {serializer.validated_data.get('agency_name')} created!'
            },
            status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
       return self.destroy(request, *args, **kwargs)

class ListProjects(GenericAPIView, ListModelMixin):
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class DetailedProjectView(GenericAPIView, DestroyModelMixin):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request, agency_name: str, project_name: str):
        serializer = serializers.ProjectSerializer(data = {'associated_agency' :  agency_name,
                                                           'project_name' : project_name})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : f'Project {serializer.validated_data.get('project_name')} for agency {serializer.validated_data.get('associated_agency')} succesfully created!'
            },
            status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)