import os
import pymongo
from pymongo.collection import Collection
from typing import Tuple
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
            password = os.getenv('MONGO_PASS'),
            authSource = 'Assets'
        )

    def _access_resource(self, collection_name: str, asset_name: str,
                         project_name: str, agency_name: str) -> Tuple[Collection, dict]:
        '''
            Considering that we use the same flow in both
            resouce creation and deletion, it is written here,.
        '''
        col = self._create_collection(collection_name)
        finalized_resource = {'agency' : agency_name, 'project' : project_name,
                              'resource_id' : asset_name}
        return (col, finalized_resource,)
    
    def _delete_resource(self, collection_name: str, asset_name: str,
                         project_name: str, agency_name: str):
        '''
            Deletes the resource with
            the passed asset name. Returns that document
            so that we can do the lookup in Minio.
        '''
        data = self._access_resource(collection_name, asset_name, project_name, agency_name)
        deleted_inst = data[0].find_one_and_delete(filter = data[1])
        return deleted_inst.get('resource_id')

    def _create_collection(self, collection_name: str) -> Collection:
        '''
            This will be called on every asset type
            in the asset view request.
            In order to avoid checking whether or not the given collection
            already exists directly inside 
        '''
        return self.__client['assets'][collection_name]

    def _insert_resource(self, agency_name: str, project_name: str,
                         asset_name: str, collection_name: str) -> None:
        '''
            After the asset was inserted in the minio, a 
            resource will be inserted into the respective collection
            map the agency/project with the given asset.
        '''
        data = self._access_resource(collection_name, asset_name, project_name, agency_name)
        data[0].insert_one(document = data[1])
        