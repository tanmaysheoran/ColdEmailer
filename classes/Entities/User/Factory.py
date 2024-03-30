from classes.Entities.UserBase.Factory import mongoDBManager
from classes.Entities.User.Model import User
from bson import ObjectId


def get_user_by_query(query) -> User:
    user_data = mongoDBManager.read_documents(query)
    if user_data:
        user_data = user_data[0]
        user = User(**user_data)
        return user
    else:
        return None


def get_user_by_id(id: ObjectId) -> User:
    return get_user_by_query({"_id": ObjectId(id)})


def get_user_by_email(email: str) -> User:
    return get_user_by_query({"email": email})
