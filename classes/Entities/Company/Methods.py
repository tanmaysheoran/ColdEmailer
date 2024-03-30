from classes.Crunchbase.API import API as CrunchbaseAPI
from classes.Entities.Company.Factory import mongoDBManager
from classes.Entities.Company.Model import Company
from bson import ObjectId
import os


def lookup(company_name: str):
    """
    Looks up a company using the Crunchbase API.

    Args:
        company_name (str): The name of the company to lookup.

    Returns:
        list: A list of dictionaries containing information about the company.
              Each dictionary contains the following keys:
              - name: The name of the company.
              - permalink: The permalink of the company.
              - uuid: The UUID of the company.
              - image_url: The URL of the company's image.
    """
    crunchbase_api = CrunchbaseAPI()
    img_url = os.environ.get('CRUNCHBASE_IMAGE_URL')
    response = crunchbase_api.autocomplete(
        company_name, ["organizations"])
    if response:
        result = [{"name": item.identifier.value, "permalink": item.identifier.permalink, "uuid": item.identifier.uuid,
                   "image_url": f"{img_url}/{item.identifier.image_id}"} for item in response.entities]
        return result
    return []


def save(company: Company) -> bool:
    """
    Saves a company to the database.

    Args:
        company (Company): The company object to save.

    Returns:
        bool: True if the company was successfully saved, False otherwise.
    """
    data = company.model_dump(by_alias=True)
    data.pop("_id")
    data.pop("people")
    update_query = {"$set": data, "$addToSet": {
        "poeple": {"$each": [item.model_dump() for item in company.people]}}}
    return mongoDBManager.update_document(new_data={"id": ObjectId(company.id)}, update_query=update_query, upsert=True)
