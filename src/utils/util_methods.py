import base64
from django.core.cache import cache
from manager.models import Project
from .manage_mongo import MongoManager
from .manage_resources import ManageMinio
from .additional_methods import get_all_formats
from django.core.files.uploadedfile import InMemoryUploadedFile

def manage_incr() -> int:
    '''
        Will increment the integer
        stored in cache. If not created, it will insert it first.
    '''
    val = cache.get('id')
    if not val:
        cache.set('id', '0', timeout = None)
        return 0
    else:
        val = int(val) + 1
        cache.set('id', str(val))
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
            resource_names = asset['resource_ids']
            asset_base_name = resource_names['base']
            response_dict[collection][asset_base_name] = dict()
            for resource_format, resource_name in resource_names.items():
                response_dict[collection][asset_base_name][f'{resource_format}'] = minio_mngr._get_resource(asset_name = resource_name,
                                                                            content_type = collection)
    return response_dict

def format_params(asset: InMemoryUploadedFile, asset_type: str, asset_id: int) -> dict:
    '''
        For the insertion process to work as a celery task,
        the params that we pass must be serializable.
        We pass a InMemoryUploadedFile type to this method (as well as other args that need formatting)
        and we transform that data, just like we previously did in ManageMinio._insert_resource.
    '''
    asset_name = asset.name.split('.')[0]
    split_type = asset.content_type.split('/')
    asset_extension, content_type = split_type[1], split_type[0]
    finalized_names = get_all_formats(asset_id = asset_id, name = asset_name, ext = asset_extension)
    asset_data = asset.read()
    asset_data_stringified = base64.b64encode(asset_data).decode('utf-8')

    finalized_dict = {'finalized_names' : finalized_names, 'asset_ext' : asset_extension, 
                      'content_type' : content_type, 'asset_data' : asset_data_stringified}
    return finalized_dict