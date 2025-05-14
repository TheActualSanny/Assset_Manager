from celery import shared_task
from .models import Project, Agency
from utils.manage_mongo import MongoManager
from utils.manage_resources import ManageMinio
from django.core.files.uploadedfile import InMemoryUploadedFile

mongo_manager = MongoManager()
minio_manager = ManageMinio()

@shared_task
def insert_resource(project_name: str, agency_name: str, asset_type: str, 
                   asset_data: str, asset_names: str):
    '''
        This will insert an asset into both MongoDB and Minio buckets.
        Both of the insert methods are called here in order to make this whole process
        a shared task for celery.
    '''
    
    # if mongo_manager.document_exists(asset_type = asset_type, asset_name = asset_names, project_name = project_name,
    #                                  agency_name = agency_name):
    #     minio_manager.update_asset(rsrc = asset_data, content_type = asset_type, asset_name = asset_names)
    # else:
    minio_manager._insert_resource(rsrc = asset_data, finalized_names = asset_names.copy(),
                                    content_type = asset_type)
    mongo_manager._insert_resource(agency_name = agency_name, project_name = project_name,
                            asset_name = asset_names, collection_name = asset_type)

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
def delete_agency_data(agency_name: str) -> None:
    '''
        Just like delete_project_data, this function
        deletes all of the assets associated with a given agency.
    '''
    projects = Project.objects.prefetch_related('associated_agency').filter(associated_agency__pk = agency_name)
    for project in projects:
        delete_project_data.delay(project_name = project.project_name)
    Agency.objects.filter(agency_name = agency_name).delete()
    