import io
import base64
from .img_transformations import ImageManager

def formatted_title(file_name: str) -> str:
    '''
        In manager classes' methods where we
        do lookups for certain assets, this method will be
        called to compare the actual names instead of blob names.
    '''
    return file_name.split('_')[1]

def get_all_formats(asset_id: int, name: str, ext: str) -> dict:
    '''
        Considering that we will have
        4 formats for each image, this dict will contain
        the formats as elements, so that we can insert the 
        actual asset names later on.
    '''
    format_dicts = {
        'base' : f'{asset_id}_{name}_blob.{ext}',
        'vertical' : f'{asset_id}_{name}_vertical_blob.{ext}',
        'landscape' : f'{asset_id}_{name}_landscape_blob.{ext}',
        'square' : f'{asset_id}_{name}_square_blob.{ext}',
        'portrait' : f'{asset_id}_{name}_portrait_blob.{ext}'
    }

    return format_dicts
