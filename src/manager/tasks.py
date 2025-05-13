from celery import shared_task
from .models import Project
from utils.manage_mongo import MongoManager
from utils.manage_resources import ManageMinio
from django.core.files.uploadedfile import InMemoryUploadedFile

mongo_manager = MongoManager()
minio_manager = ManageMinio()

@shared_task
def insert_resource(project_name: str, agency_name: str, asset_type: str, 
                   asset_data: str, asset_name: str):
    '''
        This will insert an asset into both MongoDB and Minio buckets.
        Both of the insert methods are called here in order to make this whole process
        a shared task for celery.
    '''
    minio_manager._insert_resource(rsrc = asset_data, finalized_name = asset_name,
                                                content_type = asset_type)
    mongo_manager._insert_resource(agency_name = agency_name, project_name = project_name,
                                asset_name = asset_name, collection_name = asset_type)

@shared_task    
def delete_resource(project_name: str, agency_name: str, asset_type: str,
                    asset_name: str):
    '''
        Deletes the asset that the user passed (if it exists).
    ''' 
    resource_name = mongo_manager._delete_resource(collection_name = asset_type, asset_name = asset_name,
                                                project_name = project_name, agency_name = agency_name)
    minio_manager._delete_resource(content_type = asset_type, asset_name = resource_name)

@shared_task
def delete_project_data(project_name: str) -> None:
    '''
        We pass both managers and a project name as 
        arguments, and it deletes all records associated with a given project.
    '''
    collections = mongo_manager._get_records()
    for collection_name in collections:
        records = mongo_manager._create_collection(collection_name)
        for record in records.find({'project' : project_name}):
            records.find_one_and_delete({'_id' : record['_id']})
            minio_manager._delete_resource(content_type = collection_name,
                                        asset_name = record['resource_id'])

@shared_task
def delete_agency_data(agency_name: str, mongo_mngr: MongoManager,
                       minio_mngr: ManageMinio) -> None:
    '''
        Just like delete_project_data, this function
        deletes all of the assets associated with a given agency.
    '''
    projects = Project.objects.prefetch_related('associated_agency').filter(associated_agency__pk = agency_name)
    for project in projects:
        delete_project_data(project_name = project.project_name)