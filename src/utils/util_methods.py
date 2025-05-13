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
        
def get_data(agency_name: str, lookup_type: str, 
             mongo_mngr: MongoManager, minio_mngr: ManageMinio, project_name = None) -> dict:
    '''
        Gets assets associated with the passed project.
    '''
    response_dict = dict()
    data = mongo_mngr._get_records()
    if lookup_type == 'project':
        find_condition = {'project' : project_name, 'agency' : agency_name}
    else:
        find_condition = {'agency' : agency_name}
    for collection in data:
        response_dict[collection] = dict()
        assets = mongo_mngr._create_collection(collection)
        for asset in assets.find(find_condition):
            resource_name = asset['resource_id']
            response_dict[collection][f'{resource_name}'] = minio_mngr._get_resource(asset_name = resource_name,
                                                                         content_type = collection)
    return response_dict