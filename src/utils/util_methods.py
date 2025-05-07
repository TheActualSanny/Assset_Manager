from django.core.cache import cache
from manager.models import Project
from .manage_mongo import MongoManager
from .manage_resources import ManageMinio

def manage_incr() -> int:
    '''
        Will increment the integer
        stored in cache. If not created, it will insert it first.
    '''
    val = cache.get('id')
    if not val:
        cache.set('id', '0')
        return 0
    else:
        cache.set('id', str(int(val) + 1))
        return val


def delete_project_data(project_name: str, mongo_mngr: MongoManager, 
                        minio_mngr: ManageMinio) -> None:
    '''
        We pass both managers and a project name as 
        arguments, and it deletes all records associated with a given project.
    '''
    collections = mongo_mngr._get_records()
    for collection_name in collections:
        records = mongo_mngr._create_collection(collection_name)
        for record in records.find({'project' : project_name}):
            records.find_one_and_delete({'_id' : record['_id']})
            minio_mngr._delete_resource(content_type = collection_name,
                                        asset_name = record['resource_id'])

def delete_agency_data(agency_name: str, mongo_mngr: MongoManager,
                       minio_mngr: ManageMinio) -> None:
    '''
        Just like delete_project_data, this function
        deletes all of the assets associated with a given agency.
    '''
    projects = Project.objects.prefetch_related('associated_agency').filter(associated_agency__pk = agency_name)
    for project in projects:
        delete_project_data(project_name = project.project_name, mongo_mngr = mongo_mngr,
                            minio_mngr = minio_mngr)
        
def get_agency_data(agency_name: str, mongo_mngr: MongoManager,
                    minio_mngr: ManageMinio) -> dict:
    '''
       Method which will return all of the assets associated with a given agency.
    '''
    response_dict = dict()
    data = mongo_mngr._get_records()
    for collection in data:
        response_dict[collection] = dict()
        assets = mongo_mngr._create_collection(collection)
        for asset in assets.find({'agency' : agency_name}):
            resource_name = asset['resource_id']
            response_dict[collection][f'{resource_name}'] = minio_mngr._get_resource(asset_name = resource_name,
                                                                         content_type = collection)
    return response_dict
