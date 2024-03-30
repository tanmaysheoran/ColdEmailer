from classes.MotherClass import MotherClass
from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(MotherClass):
    firstname: str
    lastname: str
    email: EmailStr
    is_verified: bool = False
