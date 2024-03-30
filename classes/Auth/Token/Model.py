from classes.MotherClass import MotherClass
from datetime import datetime
from pydantic import BaseModel
from bson import ObjectId


class Token(MotherClass):
    user_id: ObjectId
    session_id: ObjectId
    token_expiration: datetime
    firstname: str
    lastname: str
    email: str


class JWT(BaseModel):
    access_token: str
    token_type: str
