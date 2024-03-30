from classes.Entities.Company.Factory import mongoDBManager
from classes.Entities.Person.Model import Person
from bson import ObjectId


def get_person_with_company_name_by_id(person_id: ObjectId) -> tuple[Person, str]:
    """
    Retrieves a person from the database by its ID.

    Args:
        person_id (ObjectId): The ID of the person.

    Returns:
        Person: The person object if found, None otherwise.
    """
    query = {
        'poeple.id': ObjectId(person_id)
    }
    project = {
        'poeple.$': 1,
        'company_name': 1
    }
    person = mongoDBManager.read_documents(query, project)
    if person:
        person = person[0]
        return Person(**person['poeple'][0]), person['company_name']
