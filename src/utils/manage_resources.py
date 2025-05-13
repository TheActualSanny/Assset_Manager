import os
import io
import base64
from minio import Minio
from dotenv import load_dotenv
from django.core.cache import cache

load_dotenv()

class ManageMinio:
    '''
        Manages Storage/Retrieving of resources
        inside minio. Just like MongoDB, 
        a single instance will be created in views
    '''
    def __init__(self):
        '''
            The client instance is created here.
        '''
        self.__client = Minio(endpoint = f'{os.getenv('MINIO_HOST')}:9000', access_key = os.getenv('ACCESS_KEY'),
                              secret_key = os.getenv('SECRET_KEY'), secure = False)
        self._resource_name_format = '{id}_{name}_blob.{ext}'

    def _generate_name(self, asset_id: int, file_name: str, ext: str) -> str:
        '''
            Will generate a resource name based on the name of
            the file that the user passed. For this,
            the format attribute will be used.
        '''
        return self._resource_name_format.format(id = asset_id, name = file_name,
                                                 ext = ext)

    def _insert_resource(self, rsrc: str, finalized_name: str,
                         content_type: str):
        '''
            The stream bytes that the
            user sends in the request
            will be inserted inside a bucket.
            
            rsrc: The stringified file that contains the main data.
        '''
        asset_data = base64.b64decode(rsrc)
        file_like = io.BytesIO(asset_data)

        self._manage_buckets(content_type)
        self.__client.put_object(bucket_name = content_type, object_name = finalized_name,
                                 data = file_like, 
                                 length = len(asset_data))

    def _manage_buckets(self, asset_bucket: str):
        '''
            If a bucket for the passed content type doesnt exist,
            this method will create it.
        '''
        if not self.__client.bucket_exists(bucket_name = asset_bucket):
            self.__client.make_bucket(bucket_name = asset_bucket)

    def _delete_resource(self, content_type: str, asset_name: str):
        '''
            Deletes a given asset from the bucket.
        '''
        if asset_name:
            self.__client.remove_object(bucket_name = content_type, object_name = asset_name)
        else:
            print('Doesnt exist!')

    def _get_resource(self, asset_name: str, content_type: str) -> str:
        '''
            Returns an URL so that the client
            can access the resource.
        '''
        return self.__client.presigned_get_object(bucket_name = content_type, 
                                                  object_name = asset_name)

    def _resource_exists(self, blob_name: str) -> bool:
        '''
            Checks if a given resource is inserted into minio.
            This will be utilized in deletion of assets.
        '''
