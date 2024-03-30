from classes.Auth.User.Model import NewUser, AuthUser
from classes.Auth.User.Factory import get_user_by_query, get_user_by_email
from classes.Auth.PasswordHelper import Password
from classes.Auth.User.Factory import mongoDBManager
from classes.SendGrid.API import SendGrid
from fastapi import HTTPException, status
from bson import ObjectId


def get_user_by_verification_token(verification_token: ObjectId):
    return get_user_by_query({"verification_token": verification_token})


def user_already_exists(email: str):
    return get_user_by_email(email) is not None


def send_verification_email(email, token):
    sendgrid = SendGrid()
    subject = "Verify Your thehightable Account"
    content = f"""<h1>Verify your email</h1>
    <p>Click the link below to verify your email</p>
    <a href="http://localhost:8000/verify-email/{token}">Verify Email</a>"""
    return sendgrid.send_email(email, subject, content)


def verify_user(token: ObjectId):
    user = get_user_by_verification_token(token)
    if user:
        if user.is_verified:
            return "User already verified"
        if token == user.verification_token:
            user.is_verified = True
            if update(user):
                return "User verified"
            else:
                raise HTTPException(
                    status.HTTP_500_INTERNAL_SERVER_ERROR, "Error occurred while verifying user")
    raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid token")


def create_new_user(user: NewUser):
    if user_already_exists(user.email):
        raise ValueError("User already exists")

    if not Password.is_valid_password(user.password):
        raise ValueError("Password is not valid")
    user.password = Password.generate_hash(user.password)
    new_user = AuthUser(**user.model_dump())
    insered_id = mongoDBManager.insert_document(new_user.model_dump())
    if insered_id:
        send_verification_email(new_user.email, new_user.verification_token)
        return "Verification Email Sent"
    else:
        raise Exception("Error occurred while creating new user")


def update(user: AuthUser):
    return mongoDBManager.update_document(user)
