from sqlalchemy.orm import sessionmaker
from src.postgre_management.engine_creation import db_engine
from .serializers import AssetType, ValidateUploaded
from src.utils_methods.manage_resources import ManageMinio
from src.utils_methods.manage_mongo import MongoManager
from src.dependencies.redis_client import cache
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from src.utils_methods.additional_methods import validate_agency_and_project
from src.utils_methods.util_methods import manage_incr, format_params
from src.dependencies.tasks import insert_resource, delete_resource


router = APIRouter()
session = sessionmaker(bind = db_engine)()
minio_manager = ManageMinio()
mongo_manager = MongoManager()

@router.post('/add/{agency_name}/{project_name}')
async def add_asset(agency_name: str, project_name: str, 
                    asset_type: AssetType = Form(...), asset: UploadFile = File(...)):
    '''
        This will add the passed asset to the bucket and 
        MongoDB.
    '''
    validator = ValidateUploaded(passed_type = asset_type, content_type = asset.content_type)
    if validate_agency_and_project(db_session = session, agency_name = agency_name, 
                                   project_name = project_name):
        asset_id = manage_incr(cache = cache)
        formatted = await format_params(asset = asset, asset_type = asset_type, asset_id = asset_id)
        insert_resource.delay(project_name = project_name, agency_name = agency_name,
                              asset_data = formatted['asset_data'], asset_names = formatted['finalized_names'],
                              asset_type = asset_type.value, asset_ext = formatted['asset_ext'])
        return {'msg' : 'Successfully uploaded the data!'}
    

@router.delete('/delete/{agency_name}/{project_name}/{asset_name}')
async def delete_asset(agency_name: str, project_name: str,
                       asset_name: str, asset_type: AssetType = Form(...)):
    delete_resource.delay(project_name = project_name, agency_name = agency_name,
                          asset_name = asset_name, asset_type = asset_type.value)
    return {'msg' : 'Successfully deleted the assets!'}