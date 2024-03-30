from classes.Google.GenerativeAI import GoogleGenerativeAI
from classes.Entities.Person.Model import Person
import json
import os

_promt = os.environ.get("PERSON_EXTRACTION_PROMPT")


def extract_from_text(text: str, company_website: str):
    genai = GoogleGenerativeAI()
    prompt = _promt + \
        f"""the website for the company is {
            company_website}, so use this for the emails. """ + text
    response = genai.generate_content(prompt)
    json_people = json.loads(response)
    return [Person(**person) for person in json_people]
