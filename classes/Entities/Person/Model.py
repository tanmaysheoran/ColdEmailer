from classes.MotherClass import MotherClass
from pydantic import EmailStr
from typing import Optional


class Person(MotherClass):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    position: Optional[str] = None
    verified_email: Optional[EmailStr] = None
    unverified_emails: Optional[list[EmailStr]] = []
    role: Optional[str] = None
    phone: Optional[str] = None
    linkedin_link: Optional[str] = None
    location: Optional[str] = None
