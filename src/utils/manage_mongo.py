import os
import pymongo
from typing import Tuple, List
from dotenv import load_dotenv
from pymongo.collection import Collection
from .additional_methods import formatted_title

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

    def _access_resource(self, collection_name: str, asset_names: str,
                         project_name: str, agency_name: str) -> Tuple[Collection, dict]:
        '''
            Considering that we use the same flow in both
            resouce creation and deletion, it is written here,.
        '''
        col = self._create_collection(collection_name)
        finalized_resource = {'agency' : agency_name, 'project' : project_name,
                              'resource_ids' : asset_names}
        return (col, finalized_resource,)
    
    def _delete_resource(self, collection_name: str, asset_name: str,
                         project_name: str, agency_name: str):
        '''
            Deletes the resource with
            the passed asset name. Returns that document
            so that we can do the lookup in Minio.
        '''
        data = self._access_resource(collection_name, asset_name, project_name, agency_name)
        data[1].pop('resource_ids')
        for record in data[0].find(data[1]):
            resource_titles = record.get('resource_ids')
            if formatted_title(resource_titles['base']) == asset_name:
               return data[0].find_one_and_delete(filter = record).get('resource_ids')

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
    
    def _get_resource(self, asset_type: str, agency_name: str, 
                      project_name: str, asset_name: str, asset_format: str) -> str:
        '''
            Finds a requested user in the respective 
            collection.

        '''
        data = self._access_resource(collection_name = asset_type, asset_names = asset_name,
                                     project_name = project_name, agency_name = agency_name)
        found_data = dict()
        for record in data[0].find({'agency' : agency_name, 'project' : project_name}):
            asset_id = record.get('resource_ids').get(asset_format)
            if formatted_title(asset_id) == asset_name:
                return asset_id
            
    def _get_records(self) -> List[str]:
        '''
            Must make sure that it doesn't create a new collection.
        '''
        
        return self.__client['assets'].list_collection_names()
    
    def document_exists(self, asset_type: str, asset_name: str,
               project_name: str, agency_name: str) -> bool:
        '''
            Checks if a passed asset for the passed agency's project
            already exists. If it does, we will run the update_resource.
        '''
        collection = self._create_collection(asset_type)
        for document in collection.find({'agency' : agency_name, 'project' : project_name}):
            if formatted_title(document['resource_id']) == formatted_title(asset_name):
                return True
