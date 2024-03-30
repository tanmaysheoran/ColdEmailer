from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId
import logging
import os


class MongoDBManager:
    __client = None
    __db = {}
    __instance = {}

    def __new__(cls, collection_name: str, database_name: str = None):
        database_name = database_name or os.environ.get(
            'MONGODB_DATABASE_NAME')
        collection_name = collection_name or os.environ.get(
            'MONGODB_COLLECTION_NAME')
        if cls.__client is None:
            cls.create_mongo_client()
        if cls.__db.get(database_name) is None:
            cls.__db[database_name] = cls.__client[database_name]
            cls.__instance[database_name] = {}
        if cls.__instance.get(database_name).get(collection_name) is None:
            cls.__instance[database_name][collection_name] = cls.create_collection_if_not_exists(
                collection_name, database_name)

        return super().__new__(cls)

    def __init__(self, collection_name: str, database_name: str = None):
        database_name = database_name or os.environ.get(
            'MONGODB_DATABASE_NAME')
        collection_name = collection_name or os.environ.get(
            'MONGODB_COLLECTION_NAME')
        self.collection = self.__instance[database_name][collection_name]

    def insert_document(self, data):
        try:
            if isinstance(data, BaseModel):
                data = data.model_dump(by_alias=True)

            _id = data.get("id")
            if _id:
                data["_id"] = ObjectId(_id)
                del data["id"]
            inserted_document = self.collection.insert_one(data)
            logging.info("Document inserted with id:",
                         inserted_document.inserted_id)
            return inserted_document.inserted_id
        except Exception as e:
            logging.exception(
                "Error occurred while inserting document:", str(e))
            raise e

    def insert_multiple_documents(self, data):
        try:
            inserted_documents = self.collection.insert_many(data)
            logging.info("Documents inserted with ids:",
                         inserted_documents.inserted_ids)
            return inserted_documents.inserted_ids
        except Exception as e:
            logging.exception(
                "Error occurred while inserting documents:", str(e))
            raise e

    def read_documents(self, query=None, project=None):
        try:
            query["isDeleted"] = {"$ne": True}
            documents = self.read_documents_with_pagination(query, project)
            return documents
        except Exception as e:
            logging.error("Error occurred while reading documents:", str(e))
            return None

    def read_documents_with_pagination(self, query=None, project=None, page=1, limit=10):
        try:
            if query:
                documents = self.collection.find(
                    query, projection=project).skip((page-1)*limit).limit(limit)
            else:
                documents = self.collection.find().skip((page-1)*limit).limit(limit)
            return [document for document in documents]
        except Exception as e:
            logging.error("Error occurred while reading documents:", str(e))
            return None

    def update_document(self, new_data=None, query=None, update_query=None, array_filters=None, upsert=False):
        try:
            if isinstance(new_data, BaseModel):
                new_data = new_data.model_dump(by_alias=True)
            if query is None:
                query_id = new_data.get("id") or new_data.get("_id")
                query = {"_id": ObjectId(query_id)} if query_id else None
            if update_query is None:
                update_query = {"$set": new_data}
            update_result = self.collection.update_many(
                query, update_query, upsert=upsert, array_filters=array_filters)
            logging.info("Documents matched:", update_result.matched_count)
            logging.info("Documents modified:", update_result.modified_count)
            if (update_result.matched_count == 0 and not upsert):
                raise FileNotFoundError("No document found to update")
            return True
        except Exception as e:
            logging.exception(
                "Error occurred while updating documents:", str(e))
            return False

    def delete_document(self, query):
        try:
            delete_result = self.collection.delete_many(query)
            logging.info("Documents matched:", delete_result.deleted_count)
            return True
        except Exception as e:
            logging.exception(
                "Error occurred while deleting documents:", str(e))
            return False
    from bson import ObjectId

    @classmethod
    def create_mongo_client(self):
        if not self.__client:
            connection_string = os.environ.get('MONGODB_CONNECTION_STRING')
            self.__client = MongoClient(connection_string)

    @classmethod
    def create_collection_if_not_exists(self, collection_name, database_name):
        db = self.__db[database_name]
        try:
            # Check if the collection exists
            if collection_name not in db.list_collection_names():
                # If the collection does not exist, create it
                db.create_collection(collection_name)
                logging.info(
                    f"Collection '{collection_name}' created successfully.")
            else:
                logging.info(f"Collection '{collection_name}' already exists.")
            return db[collection_name]
        except Exception as e:
            logging.exception(
                f"Error occurred while creating collection '{collection_name}':", str(e))
            raise e


class MongoDBCollectionManager():
    _instance = None
    collections = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.collections = {}

    def get_mongodb_manager(self, collection_name):
        mongo_manager = self.collections.get(collection_name)
        if not mongo_manager:
            self.database_name = os.environ.get('MONGODB_DATABASE_NAME')
            self.collection_name = collection_name
            self.collections[collection_name] = MongoDBManager(
                collection_name, self.database_name)
        return self.collections[collection_name]

    def create_collections(self, collections: list[str]):
        for collection in collections:
            self.get_mongodb_manager(collection)
