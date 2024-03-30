from classes.Entities.UserEmailTemplate.Model import UserEmailTemplate
from classes.Entities.UserEmailTemplate.Methods import save_email_template_to_user
from classes.Entities.Person.Model import Person
from classes.Entities.Prompts.Model import Prompt
from classes.Entities.User.Model import User
from classes.Entities.Task.Model import Task
from classes.Entities.Task.Methods import move_to_in_progress, move_to_completed, move_to_failed
from classes.Entities.UserEmailTemplate.Methods import generate_email_body
from classes.Entities.User.Factory import get_user_by_id
from classes.Helper.FileReader import FileReader
from bson import ObjectId


def create_email_template(file: bytes, prompt: str, first_name: str, last_name: str,
                          position: str, company: str, location: str, verified_email: str = None, unverified_emails: list[str] = [],):
    file_reader = FileReader(file)
    extracted_data = file_reader.convert_and_extract()
    email_content = generate_email_body(prompt=prompt,
                                        resume_data=extracted_data["cleaned_text"], first_name=first_name, last_name=last_name, position=position, company=company, location=location)
    to_mail = verified_email if verified_email else unverified_emails.pop(
        0)

    email_template = UserEmailTemplate(
        subject=email_content["subject"], body=email_content["body"], to=to_mail, cc=unverified_emails)

    return email_template


def get_email_templates_by_user_id(user_id: ObjectId):
    user = get_user_by_id(user_id)
    return user.email_templates


def generate_and_store_email_template(file: bytes, prompt: Prompt, person: Person, user: User, company_name: str, task: Task):
    try:
        move_to_in_progress(task)
        email_template = create_email_template(file=file, prompt=prompt.prompt, verified_email=person.verified_email, unverified_emails=person.unverified_emails, first_name=person.first_name, last_name=person.last_name,
                                               position=person.position, company=company_name, location=person.location)
        result = save_email_template_to_user(email_template, user)
        move_to_completed(task, result)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        move_to_failed(task, str(e))
