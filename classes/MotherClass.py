from pydantic import BaseModel, Field
from bson import ObjectId


class MotherClass(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    isDeleted: bool = False

    class Config():
        arbitrary_types_allowed = True
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            ObjectId: str
        }
