from classes.Search.Search import Search
from classes.Entities.Task.Model import Task
from classes.Entities.Person.Methods import extract_from_text
from classes.Entities.Person.Model import Person
from classes.Entities.Task.Methods import move_to_in_progress, move_to_completed, move_to_failed
from classes.Entities.Company.Factory import get_company_info
from classes.Entities.Company.Methods import save as save_company
import logging


class LinkedInSearch():
    """
    This class represents a LinkedIn search functionality.
    It allows searching for people based on role, company, and location.
    """

    def __init__(self, role: str, company: str, location: str, pages: int, task: Task, crunchbase_uuid: str = None):
        """
        Initializes a new instance of the LinkedInSearch class.

        Args:
            role (str): The role to search for.
            company (str): The company to search for.
            location (str): The location to search in.
            pages (int): The number of pages to search.
            task (Task): The task associated with the search.
            crunchbase_uuid (str, optional): The UUID of the company in Crunchbase. Defaults to None.
        """
        self.role = role
        self.company = company
        self.crunchbase_uuid = crunchbase_uuid
        self.pages = pages
        self.task = task
        self.location = location
        self.query = f'''Current Role: {
            self.role} + {self.company} + {self.location}'''
        self.results = []

    def search(self):
        """
        Performs the LinkedIn search based on the provided parameters.
        """
        linkedin_poeple_search = Search(
            "LINKEDIN_SEARCH_ENGINE_ID", pages_to_get=self.pages, query=self.query, company=self.company, task_id=self.task.id)
        linkedin_poeple_search.search()
        self.results = linkedin_poeple_search.results

    def extract_people_from_search(self, company_website: str) -> list[Person]:
        """
        Extracts people from the search results and returns a list of Person objects.

        Args:
            company_website (str): The website of the company.

        Returns:
            list[Person]: A list of Person objects extracted from the search results.
        """
        results = []
        for result in self.results:
            try:
                results.extend(extract_from_text(
                    result.to_json(), company_website))
            except Exception as e:
                logging.error(e)
                continue
        return results

    def process(self):
        """
        Performs the search, extracts people from the search results, and saves the company and people information.
        """
        try:
            move_to_in_progress(task=self.task)
            self.search()
            company = None
            if self.crunchbase_uuid:
                company = get_company_info(
                    crunchbase_permalink=self.crunchbase_uuid)
            else:
                company = get_company_info(company_name=self.company)
            people = self.extract_people_from_search(company.website)
            for person in people:
                if not any(p.first_name == person.first_name and p.last_name == person.last_name for p in company.people):
                    person.location = self.location
                    company.people.append(person)
            if save_company(company):
                message = f"Company: {company}, People: {len(people)}"
                move_to_completed(self.task, message)
            else:
                move_to_failed(
                    self.task, "Error occurred while saving company")
        except Exception as e:
            move_to_failed(self.task, str(e))
