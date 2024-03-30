from classes.Database.MongoDBManager import MongoDBManager, MongoDBCollectionManager
from classes.Entities.Task.Model import Task
from bson import ObjectId


collection = "Tasks"
mongoDBManager: MongoDBManager = MongoDBCollectionManager(
).get_mongodb_manager(collection)


def get_task_by_id(id: str) -> Task:
    """
    Get a task by its ID.

    Args:
        id: The ID of the task.

    Returns:
        The task with the specified ID.
    """
    try:
        query = {"_id":  ObjectId(id)}
        data = mongoDBManager.read_documents(query)
        if data:
            return Task(**data[0])
    except Exception as e:
        raise e
