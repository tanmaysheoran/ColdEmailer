from classes.Helper.Serializable import Serializable
import re
import os


class GoogleSearchResult(Serializable):
    def __init__(self, data):
        self.kind = data.get("kind", "")
        self.url = data.get("url", {})
        self.queries = data.get("queries", {})
        self.context = data.get("context", {})
        self.search_information = data.get("searchInformation", {})
        self.items = [Item(item_data) for item_data in data.get("items", [])]

    def __str__(self):
        """
        Returns a string representation of the GoogleSearchResult object.
        """
        result_str = ""
        for key, value in vars(self).items():
            if key == "items":
                result_str += f"{key.capitalize()}:\n"
                for idx, item in enumerate(value):
                    result_str += f"\tItem {idx + 1}:\n"
                    result_str += str(item)
            else:
                result_str += f"{key.capitalize()}: {value}\n"
        return result_str


class Item(Serializable):
    def __init__(self, data):
        self.kind = data.get("kind", "")
        self.title = data.get("title", "")
        self.link = data.get("link", "")
        self.snippet = data.get("snippet", "")

    def __str__(self):
        """
        Returns a string representation of the Item object.
        """
        result_str = ""
        for key, value in vars(self).items():
            result_str += f"{key.replace('_', ' ').capitalize()}: {value}"
        return result_str

    def validate_link(self, pattern_key="REGEX_PATTERN"):
        """
        Validates whether the link attribute of the object matches a given pattern.

        Args:
            pattern_key (str): The key used to retrieve the regex pattern from the environment variables.
                            Default is "REGEX_PATTERN".

        Returns:
            bool: True if the link matches the pattern, False otherwise.
        """
        profile_pattern = os.environ.get(pattern_key)
        if re.match(profile_pattern, self.link):
            return True
        return False
