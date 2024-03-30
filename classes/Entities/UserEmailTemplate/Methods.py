from classes.Google.GenerativeAI import GoogleGenerativeAI
from classes.Entities.UserEmailTemplate.Model import UserEmailTemplate
from classes.Entities.User.Model import User
from classes.Entities.User.Methods import update
from classes.Entities.UserBase.Factory import mongoDBManager
from classes.Helper.DataCleaner import DataParser
from email.message import EmailMessage
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from bson import ObjectId
import json
import base64


def generate_email_body(prompt: str, first_name: str, last_name: str,
                        position: str, company: str, location: str, resume_data: str) -> dict:
    genai = GoogleGenerativeAI()
    prompt += f"I am seding this email to: {first_name} {last_name}\n"
    prompt += f"Their Position: {position}\n"
    prompt += f"Their Company: {company}\n"
    prompt += f"Their Location: {location}\n"
    prompt += f"My Resume: {resume_data}\n"
    prompt += '\n return response in JSON format WITHOUT MARKDOWN: {"subject":"", "body": ""}'
    response = genai.generate_content(prompt)
    cleaned_data = DataParser().markdown_to_text(response)
    result = json.loads(cleaned_data)
    return result


def save_email_template_to_user(email_template: UserEmailTemplate, user: User):
    user.email_templates.append(email_template)
    return update(user)


def send_email_template(email_template: UserEmailTemplate, creds: Credentials, user: User):
    try:
        service = build('gmail', 'v1', credentials=creds)

        message = EmailMessage()
        message.set_content(email_template.body)

        message["To"] = email_template.to
        if email_template.cc:
            message["Cc"] = email_template.cc
        message["Subject"] = email_template.subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(f"Email Sent: {send_message['id']}")
        user.email_templates.remove(email_template)
        email_template.sent = True
        save_email_template_to_user(email_template, user)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def update_email_template(items_to_update: dict, user_id: ObjectId, email_temaplate_id: ObjectId):
    query = {"_id": user_id, "email_templates._id": email_temaplate_id}
    update_dict = {}
    for key, value in items_to_update.items():
        update_dict[f"email_templates.$.{key}"] = value
    value = {"$set": update_dict}
    return mongoDBManager.update_document(query=query, update_query=value)
