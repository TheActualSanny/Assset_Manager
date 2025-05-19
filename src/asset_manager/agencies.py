from fastapi import APIRouter, status
from src.postgre_management.engine_creation import db_engine
from src.postgre_management.orm_setup import Agency, Project
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from .serializers import ValidateRecords
from src.utils_methods.util_methods import get_data
from src.utils_methods.manage_mongo import MongoManager
from src.utils_methods.manage_resources import ManageMinio
from src.dependencies.tasks import delete_agency_data

minio_manager = ManageMinio()
mongo_manager = MongoManager()

session = sessionmaker(bind = db_engine)

router = APIRouter()

@router.post('/add/{agency}', status_code = status.HTTP_201_CREATED)
async def add_agency(agency: str):
    '''
        Inserts a new agency into the database.
    '''
    with session() as conn:
        new_agency = Agency(agency_name = agency)
        conn.add(new_agency)
        try:
            conn.commit()
        except IntegrityError as ex:
            msg = 'Agency with the passed name already exists!'
        else:
            msg = f'Successfully added {agency}!'
    return {'msg' : msg}

@router.get('/assets/{agency}', status_code = status.HTTP_200_OK)
async def get_agency_assets(agency_name: str):
    '''
        This will return all of the assets associated with the
        passed agency.
    '''
    data = get_data(agency_name = agency_name, lookup_type = 'agency', 
                    mongo_mngr = mongo_manager, minio_mngr = minio_manager)
    return {'msg' : 'Successfully fetched the agency data!', 
            'data' : data}

@router.delete('/delete/{agency_name}')
async def delete_agency(agency_name: str):
    '''
        Deletes all of the assets associated with the passed agency
    '''
    ValidateRecords(agency_name = agency_name, project_name = None, project_validation = False)
    delete_agency_data.delay(agency_name = agency_name)
    return {'msg' : 'Successfully deleted the agency!'}