from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from .serializers import ValidateRecords
from src.postgre_management.engine_creation import db_engine
from src.postgre_management.orm_setup import Project
from src.utils_methods.additional_methods import validate_project
from src.utils_methods.util_methods import get_data
from src.utils_methods.manage_mongo import MongoManager
from src.utils_methods.manage_resources import ManageMinio
from src.dependencies.tasks import delete_project_data

minio_manager = ManageMinio()
mongo_manager = MongoManager()

router = APIRouter()
session = sessionmaker(bind = db_engine)

@router.post('/add/{agency_name}/{project_name}')
async def add_project(agency_name: str, project_name: str):
    with session() as conn:
        if validate_project(db_session = conn, agency_name = agency_name,
                        project_name = project_name):
            new_project = Project(project_name = project_name, corresponding_agency = agency_name)
            conn.add(new_project)
            conn.commit()
            msg = f'Successfully created project: {project_name} for agency: {agency_name}!'
        else:
            msg = 'Make sure to pass valid ageny/project!'
    return {'msg' : msg}

@router.get('/assets/{agency_name}/{project_name}')
async def get_project_data(agency_name: str, project_name: str):
    data = get_data(agency_name = agency_name, lookup_type = 'project',
                    mongo_mngr = mongo_manager, minio_mngr = minio_manager, project_name = project_name)
    return {'msg' : 'Successfully fetched the project data!', 
            'data' : data}

@router.delete('/delete/{agency_name}/{project_name}')
async def delete_project_assets(agency_name: str, project_name: str):
    '''
        Deletes all assets associated with the passed project.
    '''
    ValidateRecords(agency_name = agency_name, project_name = project_name)
    delete_project_data.delay(project_name = project_name, agency_name = agency_name)
    return {'msg' : 'Successfully deleted project data!'}