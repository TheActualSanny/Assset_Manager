from . import serializers
from rest_framework import status
from .models import Project, Agency
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from django.core.cache import cache
from utils.manage_incrementing import manage_incr
from utils.manage_resources import ManageMinio
from utils.manage_mongo import MongoManager
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import DestroyModelMixin, ListModelMixin

minio_manager = ManageMinio()
mongo_manager = MongoManager()

class ListAgency(GenericAPIView, ListModelMixin):
    queryset = Agency.objects.all()
    serializer_class = serializers.AgencySerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class DetailedAgencyView(GenericAPIView, DestroyModelMixin):
    queryset = Agency.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AgencySerializer

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
    serializer_class = serializers.ProjectSerializer

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
    
class AssetView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(request_body = serializers.AssetSerializer)
    def post(self, request, agency_name: str, project_name: str):
        serializer = serializers.AssetSerializer(data = request.data)
        curr_id = manage_incr()
        if not serializer.is_valid():
            return Response(serializer.errors)
        asset = serializer.validated_data.get('asset')
        asset_type = serializer.validated_data.get('asset_type')
        resource_name = minio_manager._insert_resource(asset_id = curr_id, rsrc = asset,
                                                       content_type = asset_type)
        mongo_manager._insert_resource(agency_name = agency_name, project_name = project_name, 
                                       asset_name = resource_name, collection_name = asset_type)
        return Response({'message' : 'Data successfully loaded!'})
    

class AssetViewDetailed(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(request_body = serializers.DetailedAsssetSerializer)
    def delete(self, request, agency_name: str, project_name: str, asset_name: str):
        serializer = serializers.DetailedAsssetSerializer(data = request.data)
        serializer.is_valid()
        content_type = serializer.validated_data.get('asset_type')
        print(content_type)
        resource_name = mongo_manager._delete_resource(collection_name = content_type, asset_name = asset_name,
                                                    project_name = project_name, agency_name = agency_name)
        
        minio_manager._delete_resource(content_type = content_type, asset_name = resource_name)
        return Response({'message' : 'Successfully deleted the resource!'})
    


class GetAssetView(APIView):
    permissison_classes = [IsAuthenticated]
    
    def get(self, request, agency_name: str, project_name: str, asset_name: str, asset_type: str):
        url = minio_manager._get_resource(content_type = asset_type, asset_name = asset_name)
        return Response({'url' : url})