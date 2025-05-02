import os
import pymongo
from dotenv import load_dotenv
import redis.client

load_dotenv()

class MongoManager:
    '''
        All of the essential methods for managing
        the collections will be written here.
        This is a singleton class, as one object
        will manage everything in views.py
    '''
    def __init__(self) -> pymongo.MongoClient:
        '''
            Returns a MongoDB client instance handle
            that we can then use in views.
            There will be one client instantiated in the global scope, as the MongoClient
            objects are thread-safe, so we can use a single connection accross multiple views.
        '''
        self.__client = pymongo.MongoClient(
            host = os.getenv('MONGO_HOST'),
            port = int(os.getenv('MONGO_PORT')),
            username = os.getenv('MONGO_USER'),
            password = os.getenv('MONGO_PASS')
        )

    def _create_collection(self, collection_name: str):
        '''
            This will be called on every asset type
            in the asset view request.
            In order to avoid checking whether or not the given collection
            already exists directly inside the , we check 
        '''
        return self.__client['assets'][collection_name]

    def _insert_resource(self, agency_name: str, project_name: str,
                         resource_id: int, collection_name: str) -> None:
        '''
            After the asset was inserted in the minio, a 
            resource will be inserted into the respective collection
            map the agency/project with the given asset.
        '''
        col = self._create_collection(collection_name)
        finalized_resource = {'agency' : agency_name, 'project' : project_name,
                              'resource_id' : resource_id}
        col.insert_one(document = finalized_resource)
    