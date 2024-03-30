from classes.Helper.HttpHelper import HttpHelper
from classes.Crunchbase.Entities.Organizations import Organization as OrganizationEntity
from classes.Crunchbase.Autocomplete.Autocomplete import Autocomplete
from classes.Crunchbase.Searches.Organizations import Organization as OrganizationsSearch
import json
import os


class API:
    __api_header_key = "X-cb-user-key"
    __api_url = os.environ.get("CRUNCHBASE_API_URL")
    __api_key = os.environ.get("CRUNCHBASE_API_KEY")
    __organization_search_url = __api_url + "/searches/organizations"
    __organization_entity_lookup_url = __api_url + \
        "/entities/organizations/{permalink}"
    __autocomplete_url = __api_url + "/autocompletes"

    def autocomplete(self, query: str, collection_ids: list[str] = []) -> Autocomplete:
        response = HttpHelper.get(self.__autocomplete_url, params={
                                  "query": query, "collection_ids": collection_ids}, headers={self.__api_header_key: self.__api_key})
        if response.status_code != 200:
            return None
        return Autocomplete(**response.json())

    def search_organizations(self, query: str) -> OrganizationsSearch:
        response = HttpHelper.post(self.__organization_search_url, json=query, headers={
                                   self.__api_header_key: self.__api_key})
        return OrganizationsSearch(**response.json())

    def get_organization(self, permalink: str, field_ids: list[str] = ["identifier", "location_identifiers", "short_description", "categories", "num_employees_enum", "revenue_range", "operating_status", "website", "linkedin"], card_ids: str = 'fields') -> OrganizationEntity:
        url = self.__organization_entity_lookup_url.format(permalink=permalink)
        params = {
            "field_ids": json.dumps(field_ids),
            "card_ids": card_ids
        }
        response = HttpHelper.get(url, params=params, headers={
                                  self.__api_header_key: self.__api_key})
        if response.status_code != 200:
            return None
        return OrganizationEntity(**response.json())
