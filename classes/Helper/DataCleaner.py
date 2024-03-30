from classes.Google.Search.SearchResult import GoogleSearchResult
from classes.Database.MongoDBManager import MongoDBManager
import re
import itertools
import markdown


class DataParser():
    def __init__(self, data: list[GoogleSearchResult] = []):
        self.data = data or []
        self.cleaned_data = []

    def clean(self, key_to_extract_from_items: str, regex_pattern: str, keys: list[str]):
        """
        Clean the data by extracting information from items using a regex pattern and specified keys.

        Args:
        - key_to_extract_from_items (str): The key to extract data from items.
        - regex_pattern (str): Regular expression pattern to match and extract components.
        - keys (list[str]): List of keys to extract from the regex matches.

        Returns:
        - None
        """
        # Filter out results that have items
        results = [result for result in self.data if result.items]

        # Flatten the items list
        items = list(itertools.chain.from_iterable(
            [result.items for result in results]))

        # Extract the key data from items
        key_data_for_items = [
            getattr(item, key_to_extract_from_items) for item in items if getattr(item, key_to_extract_from_items, None)]

        # Clean the data by extracting information using the extract_info method
        self.cleaned_data = self.extract_info(
            key_data_for_items, regex_pattern, keys)

    def extract_info(self, data: list[str], regex_pattern: str, keys: list[str]):
        """
        Extract information from data using a regex pattern and extract specified keys.

        Args:
        - data (list): List of strings to extract information from.
        - regex_pattern (str): Regular expression pattern to match and extract components.
        - keys (list): List of keys to extract from the regex matches.

        Returns:
        - list of dict: List of dictionaries containing extracted components.
        """
        extracted_info = []
        for item in data:
            # Using regex to extract components
            match = re.match(regex_pattern, item)
            if match:
                info = {key: match.group(idx).strip()
                        for idx, key in enumerate(keys, start=1)}
                extracted_info.append(info)
        return extracted_info

    @staticmethod
    def markdown_to_text(markdown_text):
        # Convert Markdown to HTML
        html_text = markdown.markdown(markdown_text)

        # Remove HTML tags using regular expression
        plain_text = re.sub('<[^<]+?>', '', html_text)

        return plain_text
