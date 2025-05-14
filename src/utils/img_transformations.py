import io
import base64
from PIL import Image, ImageFilter
from .additional_methods import b64_to_iobytes

class ImageManager:
    def to_portrait(self, img_data: str) -> str:
        '''
            Will rotate the image for it to be in portrait (vertical) mode.
        '''
        data = b64_to_iobytes(img_data)
        
        with Image.open(data) as img:
            img.rotate(90, expand = True)
            modified_img = img.tobytes()
        return base64.encode(modified_img).decode('utf-8')

    def to_landscape(self, img_data: str) -> str:
        '''
            Will rotate the image for it to be in landscape (horizontal) mode.
        '''
        data = b64_to_iobytes(img_data)

        with Image.open(data) as img:
            img.rotate(-90, expand = True)
            modified_img = img.tobytes()
        return base64.encode(modified_img).decode('utf-8')
    
    def to_square(self, img_data: str) -> str:
        '''
            Will crop an image for it to be a square.
            It will use the X axis for the dimensions.
        '''
        data = b64_to_iobytes(img_data)

        with Image.open(data) as img:
            x_axis = img.size[0]
            img.resize(size = (x_axis, x_axis,))
            modified_img = img.tobytes()
        return base64.b64encode(modified_img).decode('utf-8')
    
    def to_portrait(self, img_data: str) -> str:
        '''
            For now, this method blurs the image. It will apply portrait effect to it.
        '''
        data = b64_to_iobytes(img_data)

        with Image.open(data) as img:
            img.filter(ImageFilter.GaussianBlur(radius = 10))
            modified_img = img.tobytes()
        return base64.b64encode(modified_img).decode('utf-8')
    
