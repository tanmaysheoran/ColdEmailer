from classes.Auth.Session.Model import Session
from classes.Entities.UserBase.Model import UserBase
from pydantic import EmailStr, BaseModel
from typing import Optional
from bson import ObjectId


class AuthUser(UserBase):
    password: str
    active_sessions: list[Session] = []
    inactive_sessions: list[Session] = []
    verification_token: ObjectId = ObjectId()
    google_auth_credentials: Optional[dict] = None


class NewUser(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
