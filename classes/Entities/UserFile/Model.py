from bson import ObjectId
from classes.Entities.GridFSFile.Model import GridFSFile


class UserFile(GridFSFile):
    userId: ObjectId
