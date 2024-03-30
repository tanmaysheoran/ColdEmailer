from classes.Entities.Task.Model import Task
from classes.Entities.Task.Factory import mongoDBManager
from bson import ObjectId
from datetime import datetime, timezone


def save(task: Task) -> ObjectId:
    """
    saves the task into the database.

    Returns:
        The ID of the saved task.
    """
    try:
        data = task.model_dump()
        task_id = mongoDBManager.insert_document(data)
        return task_id
    except Exception as e:
        raise e


def update(task: Task) -> bool:
    """
    Update the task in the database.

    Returns:
        Boolean value indicating if the update was successful.
    """
    try:
        return mongoDBManager.update_document(task.model_dump())
    except Exception as e:
        raise e


def update_task_status(task: Task, status: str, output=None) -> bool:
    """
    Update the task status, output, and end time, and update the database.

    Args:
        status: The new status for the task.
        output: The output data for the task (optional).

    Returns:
        Boolean value indicating if the update was successful.
    """
    task.status = status
    if output is not None:
        task.output = output
    task.end_time = datetime.now(timezone.utc)
    return update(task)


def move_to_in_progress(task: Task) -> bool:
    """
    Move the task to the 'in_progress' status and update the database.

    Returns:
        Boolean value indicating if the update was successful.
    """
    return update_task_status(task, "in_progress")


def move_to_completed(task: Task, output) -> bool:
    """
    Move the task to the 'completed' status, update the output and end time, and update the database.

    Args:
        output: The output data for the task.

    Returns:
        Boolean value indicating if the update was successful.
    """
    return update_task_status(task, "completed", output)


def move_to_failed(task: Task, output) -> bool:
    """
    Move the task to the 'failed' status, update the output and end time, and update the database.

    Args:
        output: The output data for the task.
    """
    return update_task_status(task, "failed", output)
