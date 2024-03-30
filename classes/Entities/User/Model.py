from classes.Entities.UserBase.Model import UserBase
from classes.Entities.UserEmailTemplate.Model import UserEmailTemplate
from bson import ObjectId
from typing import List, Optional


class PublicUser(UserBase):
    imageId: Optional[ObjectId] = None


class User(PublicUser):
    email_templates: List[UserEmailTemplate] = []
