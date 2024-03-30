from classes.Entities.User.Model import User
from classes.Entities.UserBase.Factory import mongoDBManager
from classes.Database.MongoDBGridFSManager import MongoDBGridFSManager
from classes.Entities.UserFile.Model import UserFile
from bson import ObjectId

grid_fs = MongoDBGridFSManager()


def update(user: User, query=None):
    return mongoDBManager.update_document(user, query=query)


def update_by_id(id: ObjectId, data: dict):
    query = {"_id": id}
    return mongoDBManager.update_document(data, query)


def upload_file(file_bytes: bytes, filename: str, user_id: str, tags=[]):
    file_id = grid_fs.insert_file(
        file_bytes, filename, metadata={"userId": user_id, "tags": tags})
    return file_id


def get_file_list(user_id: str, tags=[]):
    query = {"userId": user_id, "tags": {
        "$in": tags}, "isDeleted": {"$ne": True}}
    files = grid_fs.get_file_list_by_query(query=query)
    files = [UserFile(**file) for file in files]
    return files


def get_file_bytes_by_id(file_id: str):
    file_grid_out = grid_fs.get_file_by_id(file_id)
    return file_grid_out.read()
