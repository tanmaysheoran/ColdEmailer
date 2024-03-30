from classes.Google.Search.CustomSearch import GoogleCustomSearch
from bson.objectid import ObjectId
import os


class Search():
    def __init__(self, search_engine_id: str, task_id: ObjectId, pages_to_get: int = 10, **kwargs):
        self.pages_to_get = pages_to_get
        self.search_engine_id = os.environ.get(search_engine_id)
        self.__dict__['properties'] = kwargs
        self.google_custom_search = GoogleCustomSearch(self.search_engine_id)
        self.task_id = task_id
        self.results = []

    def __getattr__(self, name):
        """
        Retrieves the value of an attribute dynamically.

        Args:
            name (str): The name of the attribute.

        Returns:
            The value of the attribute.

        Raises:
            AttributeError: If the attribute does not exist.
        """
        if name in self.__dict__:
            return self.__dict__[name]
        elif name in self.properties:
            return self.properties[name]
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Sets the value of an attribute.

        Args:
            name (str): The name of the attribute.
            value: The value to be set.
        """
        if name == 'properties':
            super().__setattr__(name, value)
        else:
            self.__dict__[name] = value

    def __delattr__(self, name):
        """
        Deletes an attribute.

        Args:
            name (str): The name of the attribute.

        Raises:
            AttributeError: If the attribute does not exist.
        """
        if name in self.properties:
            del self.properties[name]
        else:
            raise AttributeError(
                f"'{self.__class__.__name__}' object has no attribute '{name}'")

    @property
    def query(self):
        """
        Generates the search query based on the properties.

        Returns:
            str: The search query.
        """
        return " + ".join([f"{value}" for key, value in self.properties.items()])

    def search(self):
        """
        Performs a search using the Google Custom Search API.

        Updates the 'results' attribute with the search results.
        """
        self.results = self.google_custom_search.search(
            self.query, self.pages_to_get)

    def save(self):
        """
        Saves the search results to a database.

        Returns:
            list: The inserted IDs of the saved results.
        """
        inserted_ids = self.google_custom_search.save(
            self.results, params=self.properties, task_id=self.task_id)
        return inserted_ids
