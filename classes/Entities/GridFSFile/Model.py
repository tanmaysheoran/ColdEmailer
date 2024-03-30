from classes.MotherClass import MotherClass
from bson import ObjectId
from datetime import datetime


class GridFSFile(MotherClass):
    filename: str
    tags: list[str]
    chunkSize: int
    length: int
    uploadDate: datetime
