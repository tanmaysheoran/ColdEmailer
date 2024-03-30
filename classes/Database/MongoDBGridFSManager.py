from pymongo import MongoClient
from gridfs import GridFS, GridOut, Collection
from bson import ObjectId
import os


class MongoDBGridFSManager:
    __client = None
    __db = {}
    __instance = {}

    def __new__(cls, database_name: str = None):
        database_name = database_name or os.environ.get(
            'MONGODB_GRIDFS_DATABASE_NAME')
        cls.collection_name = os.environ.get(
            'MONGODB_GRIDFS_COLLECTION_NAME')
        if cls.__client is None:
            cls.create_mongo_client()
        if database_name not in cls.__db:
            cls.__db[database_name] = cls.__client[database_name]
            cls.__instance[database_name] = GridFS(cls.__db[database_name])

        return super().__new__(cls)

    def __init__(self, database_name: str = None):
        database_name = database_name or os.environ.get(
            'MONGODB_GRIDFS_DATABASE_NAME')
        self.grid_fs: GridFS = self.__instance[database_name]
        self.collection: Collection = self.__db[database_name][self.collection_name]

    @classmethod
    def create_mongo_client(self):
        if not self.__client:
            connection_string = os.environ.get('MONGODB_CONNECTION_STRING')
            self.__client = MongoClient(connection_string)

    def insert_file(self, file: bytes, filename: str, metadata: dict = None):
        try:
            file_id = self.grid_fs.put(
                file, filename=filename, **metadata)
            return file_id
        except Exception as e:
            raise e

    def get_file_by_query(self, query: dict) -> GridOut:
        try:
            file = self.collection.find_one(query)
            return file
        except Exception as e:
            raise e

    def get_file_by_id(self, file_id: ObjectId) -> GridOut:
        try:
            file_id = ObjectId(file_id)
            file = self.grid_fs.get(file_id)
            return file
        except Exception as e:
            raise e

    def get_file_list_by_query(self, query: dict) -> list[GridOut]:
        try:
            file_list = self.collection.find(query)
            return list(file_list)
        except Exception as e:
            raise e

    def calculate_file_size(self, length, chunk_size):
        # Calculate the number of full chunks
        number_of_chunks = length // chunk_size

        # Calculate the size of the last chunk
        last_chunk_size = length % chunk_size

        # Calculate the total file size
        file_size = (number_of_chunks * chunk_size) + last_chunk_size

        return file_size
