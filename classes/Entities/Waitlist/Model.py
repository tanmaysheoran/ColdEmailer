from classes.MotherClass import MotherClass
from pydantic import EmailStr


class Waitlist(MotherClass):
    name: str
    email: EmailStr
    location: str
