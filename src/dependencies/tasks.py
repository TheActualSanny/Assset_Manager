from .celery import celery_app
from src.postgre_management.engine_creation import db_engine
from sqlalchemy.orm import sessionmaker
from src.postgre_management.orm_setup import Project, Agency
from src.utils_methods.manage_mongo import MongoManager
from src.utils_methods.manage_resources import ManageMinio


mongo_manager = MongoManager()
minio_manager = ManageMinio()
session = sessionmaker(bind = db_engine)


@celery_app.task
def insert_resource(project_name: str, agency_name: str, asset_type: str, 
                   asset_data: str, asset_names: str, asset_ext: str):
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
                                    content_type = asset_type, asset_ext = asset_ext)
    mongo_manager._insert_resource(agency_name = agency_name, project_name = project_name,
                            asset_name = asset_names, collection_name = asset_type)

@celery_app.task    
def delete_resource(project_name: str, agency_name: str, asset_type: str,
                    asset_name: str):
    '''
        Deletes the asset that the user passed (if it exists).
    ''' 
    resource_names = mongo_manager._delete_resource(collection_name = asset_type, asset_name = asset_name,
                                                project_name = project_name, agency_name = agency_name)
    minio_manager._delete_resource(content_type = asset_type, asset_names = resource_names)

@celery_app.task
def delete_project_data(project_name: str, agency_name: str) -> None:
    '''
        We pass both managers and a project name as 
        arguments, and it deletes all records associated with a given project.
    '''
    collections = mongo_manager._get_records()
    for collection_name in collections:
        records = mongo_manager._create_collection(collection_name)
        for record in records.find({'project' : project_name, 'agency' : agency_name}):
            records.find_one_and_delete({'_id' : record['_id']})
            asset_ids = record['resource_ids']
            minio_manager._delete_resource(content_type = collection_name,
                                           asset_names = asset_ids)

@celery_app.task
def delete_agency_data(agency_name: str) -> None:
    '''
        Just like delete_project_data, this function
        deletes all of the assets associated with a given agency.
    '''
    with session() as conn:
        projects = conn.query(Project).filter(Project.associated_agency == agency_name).all()
        for project in projects:
            delete_project_data.delay(project_name = project.project_name, agency_name = agency_name)
        conn.query(Agency).filter(agency_name == agency_name).delete()
