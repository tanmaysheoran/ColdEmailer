from classes.Database.MongoDBManager import MongoDBCollectionManager, MongoDBManager
from classes.Entities.Prompts.Model import Prompt, PublicPrompt
from bson import ObjectId

collection = "Prompts"
mongoDBManager: MongoDBManager = MongoDBCollectionManager(
).get_mongodb_manager(collection)


def get_prompt_by_id(id: str):
    """
    Retrieves a prompt from the database by its ID.

    Args:
        id (str): The ID of the prompt.

    Returns:
        Prompt: The prompt object if found, None otherwise.
    """
    prompt = mongoDBManager.read_documents({"_id": ObjectId(id)})
    if prompt:
        prompt = prompt[0]
        return Prompt(**prompt)


def get_promt_by_tag(tags: str):
    """
    Retrieves a prompt from the database by its tag.

    Args:
        tag (str): The tag of the prompt.

    Returns:
        Prompt: The prompt object if found, None otherwise.
    """
    query = {"tags": {
        "$in": tags}}
    prompts = mongoDBManager.read_documents(query=query)
    if prompts:
        return [PublicPrompt(**prompt) for prompt in prompts]
