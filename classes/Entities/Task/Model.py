from classes.MotherClass import MotherClass
from datetime import datetime, timezone
from bson import ObjectId
from pydantic import Field
from typing import Optional, Any


class Task(MotherClass):
    """
    Represents a task in the system.

    Attributes:
        status (str): The status of the task.
        method (str): The method associated with the task.
        input (Any): The input data for the task.
        output (Any): The output data for the task.
        start_time (datetime): The start time of the task.
        end_time (datetime): The end time of the task.
        id (ObjectId): The ID of the task in the database.
    """

    status: str = "queued"
    method: str
    input: str
    output: Optional[Any] = None
    start_time: datetime = datetime.now(timezone.utc)
    end_time: Optional[datetime] = None
