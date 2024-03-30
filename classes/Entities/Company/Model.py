from classes.MotherClass import MotherClass
from classes.Entities.Person.Model import Person
from bson import ObjectId
from pydantic import Field, SerializeAsAny
from typing import Optional, List


class Company(MotherClass):
    crunchbase_uuid: Optional[str] = None
    company_name: str
    description: Optional[str] = None
    crunchbase_image_url: Optional[str] = None
    crunchbase_permalink: Optional[str] = None
    website: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    continent: Optional[str] = None
    linkedin_profile: Optional[str] = None
    people: Optional[List[SerializeAsAny[Person]]] = []
