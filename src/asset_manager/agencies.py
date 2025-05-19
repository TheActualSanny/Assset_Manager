from fastapi import APIRouter, status
from src.postgre_management.engine_creation import db_engine
from src.postgre_management.orm_setup import Agency, Project
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

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

@router.delete('/delete/{agency}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_agency(agency: str):
    '''
        For now, this only removes the record
        from the table. It will however schedule a celery task which will
        delete both minio assets and MongoDB records.
    '''
    with session() as conn:
        record = conn.query(Agency).filter(Agency.agency_name == agency).delete()
        if not record:
            msg = f'No agency with the name: {agency} was found!'
        else:
            msg = f'Successfully deleted the agency {agency}'
        conn.commit()
    return {'msg' : msg}

@router.get('/assets/{agency}', status_code = status.HTTP_200_OK)
async def get_agency_assets(agency: str):
    '''
        This will return all of the assets associated with the
        passed agency.
    '''
