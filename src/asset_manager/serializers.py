from enum import Enum
from typing import List, Any
from fastapi import UploadFile, HTTPException, status
from pydantic import BaseModel, model_validator, field_validator

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
    