from googleapiclient.discovery import build
from classes.Google.Search.SearchResult import GoogleSearchResult
from classes.Database.MongoDBManager import MongoDBManager
from bson.objectid import ObjectId
import os


class GoogleCustomSearch:
    __task_collection = "SearchResults"
    __mongoManager: MongoDBManager = None

    def __new__(cls, search_engine_id=None):
        """
        Creates a new instance of the GoogleCustomSearch class.

        Args:
            search_engine_id (str): The ID of the custom search engine.

        Returns:
            GoogleCustomSearch: The new instance of the GoogleCustomSearch class.
        """
        if not cls.__mongoManager:
            cls.__mongoManager = MongoDBManager(cls.__task_collection)

        instance = super().__new__(cls)
        return instance

    def __init__(self, search_engine_id=None):
        """
        Initializes a new instance of the GoogleCustomSearch class.

        Args:
            search_engine_id (str): The ID of the custom search engine.
        """
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        self.search_engine_id = search_engine_id or "GOOGLE_SEARCH_ENGINE_ID"
        self.service = build("customsearch", "v1", developerKey=self.api_key)

    def search_with_index(self, query, start_index):
        """
        Performs a search with a specified query and start index.

        Args:
            query (str): The search query.
            start_index (int): The start index of the search results.

        Returns:
            GoogleSearchResult: The search results.
        """
        response = self.service.cse().list(
            q=query, cx=self.search_engine_id, start=start_index).execute()
        return GoogleSearchResult(response)

    def search(self, query: str, pages_to_get: int):
        """
        Performs a search with a specified query and number of pages to get.

        Args:
            query (str): The search query.
            pages_to_get (int): The number of pages to get.

        Returns:
            list[GoogleSearchResult]: The search results for each page.
        """
        results = []
        for i in range(0, pages_to_get):
            results.append(self.search_with_index(query, i + 1))
        return results

    def save(self, search_results: list[GoogleSearchResult], params: dict, task_id: ObjectId):
        """
        Saves the search results to the database.

        Args:
            search_results (list[GoogleSearchResult]): The search results to save.
            params (dict): Additional parameters to include in the saved document.
            task_id (ObjectId): The ID of the task associated with the search results.

        Returns:
            list[ObjectId]: The IDs of the inserted documents.
        """
        try:
            data = []
            for result in search_results:
                for item in result.items:
                    if item.validate_link() and item.to_dict() not in data:
                        data.append(item.to_dict())
            doc = {"results": data, "task_id": task_id}
            doc.update(params)
            inserted_ids = self.__mongoManager.insert_multiple_documents([doc])
            return inserted_ids
        except Exception as e:
            raise e

    def get_all(self, query: dict = None, page: int = 1, limit: int = 10):
        """
        Gets all the search results from the database with pagination.

        Returns:
            list: The search results.
        """
        return self.__mongoManager.read_documents_with_pagination(query, page, limit)
