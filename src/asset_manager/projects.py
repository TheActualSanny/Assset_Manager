from fastapi import APIRouter
from sqlalchemy.orm import sessionmaker
from src.postgre_management.engine_creation import db_engine
from src.postgre_management.orm_setup import Project
from src.utils_methods.additional_methods import validate_project

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
