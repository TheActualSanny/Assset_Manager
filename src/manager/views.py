from . import serializers
from rest_framework import status
from .models import Project, Agency
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from django.core.cache import cache
from utils.manage_resources import ManageMinio
from utils.manage_mongo import MongoManager
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import DestroyModelMixin, ListModelMixin
from utils.util_methods import manage_incr, get_data, format_params
from .tasks import insert_resource, delete_resource, delete_agency_data, delete_project_data

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

    def get(self, request, pk: str):
        serializer = serializers.AgencySerializer(data = {'agency_name' : pk},
                                                  context = {'request_type' : 'GET'})
        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_404_NOT_FOUND)
        data = get_data(agency_name = pk, mongo_mngr = mongo_manager,
                        minio_mngr = minio_manager, lookup_type = 'agency')
        return Response(data = data,
                        status = status.HTTP_200_OK)
        

    def post(self, request, pk: str):
        serializer = serializers.AgencySerializer(data = {'agency_name' : pk},
                                                  context = {'request_type' : 'POST'})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : f'Agency {serializer.validated_data.get('agency_name')} created!'
            },
            status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk: str):
       delete_agency_data.delay(agency_name = pk)
       return Response({'message' : 'Successfully deleted agency data!'})

class ListProjects(GenericAPIView, ListModelMixin):
    queryset = Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class DetailedProjectView(GenericAPIView, DestroyModelMixin):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, agency_name: str, pk: str):
        serializer = serializers.ProjectSerializer(data = {'associated_agency' : agency_name,
                                                           'project_name' : pk}, 
                                                           context = {'request_type' : 'GET'})
        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        data = get_data(project_name = pk, agency_name = agency_name, lookup_type = 'project',
                        mongo_mngr = mongo_manager, minio_mngr = minio_manager)
        return Response(data = data, status = status.HTTP_200_OK)
        
    def post(self, request, agency_name: str, pk: str):
        serializer = serializers.ProjectSerializer(data = {'associated_agency' :  agency_name,
                                                           'project_name' : pk}, 
                                                           context = {'request_type' : 'POST'})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message' : f'Project {serializer.validated_data.get('project_name')} for agency {serializer.validated_data.get('associated_agency')} succesfully created!'
            },
            status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        delete_project_data.delay(project_name = kwargs.get('pk'), agency_name = kwargs.get('agency_name'))
        return self.destroy(request, *args, **kwargs)
    
class AssetView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(request_body = serializers.AssetSerializer)
    def post(self, request, agency_name: str, project_name: str):
        serializer = serializers.AssetSerializer(data = request.data,
                                                 context = {'agency' : agency_name, 'project' : project_name})
        
        curr_id = manage_incr()
        if not serializer.is_valid():
            return Response(serializer.errors)
        asset = serializer.validated_data.get('asset')
        asset_type = serializer.validated_data.get('asset_type')
        formatted_params = format_params(asset = asset, asset_type = asset_type, 
                                         asset_id = curr_id)
        insert_resource.delay(project_name = project_name, agency_name = agency_name, asset_type = formatted_params['content_type'],
                              asset_names = formatted_params['finalized_names'], asset_data = formatted_params['asset_data'],
                              asset_ext = formatted_params['asset_ext'])
        return Response({'message' : 'Data successfully loaded!'})
    

class AssetViewDetailed(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(request_body = serializers.DetailedAsssetSerializer)
    def delete(self, request, agency_name: str, project_name: str, asset_name: str):
        serializer = serializers.DetailedAsssetSerializer(data = request.data, 
                                                          context = {'project' : project_name, 'agency' : agency_name})
        if not serializer.is_valid():
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        content_type = serializer.validated_data.get('asset_type')
        delete_resource.delay(project_name = project_name, agency_name = agency_name, asset_type = content_type,
                              asset_name = asset_name)
        return Response({'message' : 'Successfully deleted the resource!'})
    

class GetAssetView(APIView):
    permissison_classes = [IsAuthenticated]
    
    def get(self, request, agency_name: str, project_name: str, asset_name: str, asset_type: str,
            asset_format: str):
        finalized_asset_name = mongo_manager._get_resource(asset_type = asset_type, agency_name = agency_name,
                                                           project_name = project_name, asset_name = asset_name, asset_format = asset_format)
        url = minio_manager._get_resource(content_type = asset_type, asset_name = finalized_asset_name)
        return Response({'url' : url})