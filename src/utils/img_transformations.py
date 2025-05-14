import io
import base64
from typing import Tuple
from PIL import Image, ImageFilter

class ImageManager:

    @staticmethod
    def load_base(img_data: str) -> str:
        data = base64.b64decode(img_data)
        return (data, io.BytesIO(data),)
    
    @staticmethod
    def to_vertical(img_data: str) -> Tuple[str, str]:
        '''
            Will rotate the image for it to be in portrait (vertical) mode.
        '''
        #TODO: Must pass the valid extension 
        with Image.open(img_data) as img:
            new_img = img.rotate(90, expand = True)
            new_stream = io.BytesIO()
            new_img.save(new_stream, format = 'jpeg')
            new_stream.seek(0)
        return base64.b64encode(new_stream.getvalue()).decode('utf-8')

    @staticmethod
    def to_landscape(img_data: str) -> str:
        '''
            Will rotate the image for it to be in landscape (horizontal) mode.
        '''
        with Image.open(img_data) as img:
            new_img = img.rotate(-90, expand = True)
            new_stream = io.BytesIO()
            new_img.save(new_stream, format = 'jpeg')
            new_stream.seek(0)
        return base64.b64encode(new_stream.getvalue()).decode('utf-8')
    
    @staticmethod
    def to_square(img_data: str) -> str:
        '''
            Will crop an image for it to be a square.
            It will use the X axis for the dimensions.
        '''
        with Image.open(img_data) as img:
            x_axis = img.size[0]
            new_img = img.resize(size = (x_axis, x_axis,))
            new_stream = io.BytesIO()
            new_img.save(new_stream, format = 'jpeg')
            new_stream.seek(0)
        return base64.b64encode(new_stream.getvalue()).decode('utf-8')
    
    @staticmethod
    def to_portrait(img_data: str) -> str:
        '''
            For now, this method blurs the image. It will apply portrait effect to it.
        '''
        with Image.open(img_data) as img:
            new_img = img.filter(ImageFilter.GaussianBlur(radius = 10))
            new_stream = io.BytesIO()
            new_img.save(new_stream, format = 'jpeg')
            new_stream.seek(0)
        return base64.b64encode(new_stream.getvalue()).decode('utf-8')
    
