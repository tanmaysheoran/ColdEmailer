from classes.Database.MongoDBManager import MongoDBCollectionManager, MongoDBManager
from classes.Crunchbase.API import API as CrunchbaseAPI
from classes.Entities.Company.Model import Company
from bson import ObjectId

collection = "Companies"
mongoDBManager: MongoDBManager = MongoDBCollectionManager(
).get_mongodb_manager(collection)


def get_company_by_id(id: str):
    """
    Retrieves a company from the database by its ID.

    Args:
        id (str): The ID of the company.

    Returns:
        Company: The company object if found, None otherwise.
    """
    company = mongoDBManager.read_documents({"_id": ObjectId(id)})
    if company:
        company = company[0]
        return Company(**company)


def get_all_companies(page: int = 1, limit: int = 10) -> list[Company]:
    """
    Retrieves all companies from the database with pagination.

    Args:
        page (int): The page number.
        limit (int): The maximum number of companies to retrieve.

    Returns:
        list: A list of company objects.
    """
    companies = mongoDBManager.read_documents_with_pagination(
        page=page, limit=limit)
    return [Company(**company) for company in companies]


def crunchbase_search_orgranization(permalink: str) -> Company:
    """
    Searches for an organization on Crunchbase by permalink.

    Args:
        permalink (str): The permalink of the organization.

    Returns:
        Company: The company object with information from Crunchbase.
    """
    crunchbase_api = CrunchbaseAPI()
    response = crunchbase_api.get_organization(permalink)
    company = Company(company_name=permalink)
    if response:
        company.company_name = response.identifier.value
        company.crunchbase_uuid = response.identifier.uuid
        company.crunchbase_permalink = response.identifier.permalink
        company.description = response.short_description
        company.crunchbase_image_url = response.cards.fields.image_url
        company.website = response.cards.fields.website_url

        for location_identifier in response.location_identifiers:
            if hasattr(company, location_identifier.location_type):
                setattr(company, location_identifier.location_type,
                        location_identifier.value)
    return company


def get_company_info(company_name: str = None, crunchbase_permalink: str = None) -> Company:
    """
    Retrieves company information from the database or Crunchbase.

    Args:
        company_name (str): The name of the company.
        crunchbase_permalink (str): The permalink of the company on Crunchbase.

    Returns:
        Company: The company object with information from the database or Crunchbase.
    """
    company = None
    if company_name:
        company = mongoDBManager.read_documents(
            {"company_name": {"$regex": company_name, "$options": "i"}})
    elif crunchbase_permalink:
        company = mongoDBManager.read_documents(
            {"crunchbase_permalink": {"$regex": crunchbase_permalink, "$options": "i"}})
    if company:
        company = company[0]
        return Company(**company)
    else:
        return crunchbase_search_orgranization(
            crunchbase_permalink or company_name)
