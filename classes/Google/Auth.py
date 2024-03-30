from classes.Auth.User.Model import AuthUser
from classes.Auth.User.Factory import get_user_by_id
from classes.Auth.User.Methods import update as update_user
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from bson import ObjectId
import pickle
import base64
import json
import os


class Auth:
    def __init__(self, state=None, encoded_state=None):
        self.scopes = ['https://www.googleapis.com/auth/gmail.send']
        self.flow = InstalledAppFlow.from_client_secrets_file(
            'classes/Google/credentials.json',
            scopes=self.scopes,
            redirect_uri=os.environ.get("GOOGLE_REDIRECT_URL")
        )
        if state:
            self.state = self.encode_state(state)
        if encoded_state:
            self.state = self.decode_state(encoded_state)

    def get_auth_url(self):
        auth_url, _ = self.flow.authorization_url(
            access_type='offline', prompt='consent', state=self.state)
        return auth_url

    def get_credentials_json(self, code):
        self.flow.fetch_token(code=code)
        return json.loads(self.flow.credentials.to_json())

    def encode_state(self, json_data: dict):
        json_dump = json.dumps(json_data)
        byte_data = pickle.dumps(json_dump)
        return base64.b64encode(byte_data)

    def decode_state(self, encoded_data: str):
        base64_decoded = base64.b64decode(encoded_data)
        pickle_load = pickle.loads(base64_decoded)
        json_data = json.loads(pickle_load)
        return json_data

    def save_credentials(self, credentials: dict, user: AuthUser):
        user.google_auth_credentials = credentials
        return update_user(user)

    def validate_credentials(self, user: AuthUser, return_credentials=False):
        if not user.google_auth_credentials:
            return False

        try:
            credentials = Credentials.from_authorized_user_info(
                user.google_auth_credentials, self.scopes)
        except Exception as e:
            print(f"Error creating credentials: {e}")
            return False

        if credentials.expired and credentials.refresh_token:
            self.refresh_credentials(user, credentials)

        if credentials.valid:
            if return_credentials:
                return credentials
            return True

        return False

    def refresh_credentials(self, user: AuthUser, credentials: Credentials):
        try:
            credentials.refresh(Request())
            user.google_auth_credentials = json.loads(credentials.to_json())
            if update_user(user):
                return True
            else:
                raise Exception("Error updating user")
        except Exception as e:
            print(f"Error refreshing credentials: {e}")
            return False

    def get_user_credentials(self, user: AuthUser = None, user_id: ObjectId = None):
        if not user and user_id is not None:
            user = get_user_by_id(user_id)
        credentials = self.validate_credentials(user, return_credentials=True)
        if credentials:
            return credentials
