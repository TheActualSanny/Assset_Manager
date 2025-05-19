from enum import Enum
from typing import List, Any, Optional
from fastapi import UploadFile, HTTPException, status
from pydantic import BaseModel, model_validator, field_validator
from sqlalchemy.orm import sessionmaker
from src.postgre_management.engine_creation import db_engine
from src.postgre_management.orm_setup import Agency, Project

session = sessionmaker(bind = db_engine)

class AssetType(Enum):
    image = 'image'
    video = 'video'
    voice = 'voice'
    music = 'music'
    logo = 'logo'

class ValidateUploaded(BaseModel):
    '''
        Checks if the passed type
        matches the type of the uploaded file.
    '''
    passed_type: AssetType
    content_type: str
    
    @model_validator(mode = 'before')
    def validate_types(cls, data: Any) -> HTTPException | Any:
        modified_type = data.get('content_type').split('/')[0]
        if modified_type != data.get('passed_type').value:
            raise HTTPException(detail = 'Make sure that the passed types match!',
                                status_code = status.HTTP_400_BAD_REQUEST)
        return data
    
class ValidateRecords(BaseModel):
    '''
        We use this one model to
        validate both passed agencies and
        passed projects.
    '''
    agency_name: str
    project_name: Optional[str]
    project_validation: bool = True

    @model_validator(mode = 'before')
    def validate_project(cls, data: Any) -> HTTPException | Any:
        with session() as conn:
            agency_filter = conn.query(Agency).filter(Agency.agency_name == data['agency_name']).first()
            if data.get('project_validation'):
                project_filter = conn.query(Project).filter(Project.project_name == data['project_name'])
                conditions = (agency_filter,
                             project_filter.filter(Project.associated_agency == data['agency_name']).first())
                if not all(conditions):
                    raise HTTPException(detail = 'Make sure to pass valid project/agency!',
                                        status_code = status.HTTP_400_BAD_REQUEST)
            else:
                if not agency_filter:
                    raise HTTPException(detail = 'Make sure to pass a valid agency!',
                                        status_code = status.HTTP_400_BAD_REQUEST)
            return data