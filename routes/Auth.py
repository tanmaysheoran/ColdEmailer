from bson import ObjectId
from classes.Auth.User.Model import NewUser
from classes.Auth.User.Methods import create_new_user, verify_user
from classes.Auth.User.Factory import get_user_by_email, get_user_by_id
from classes.Auth.Session.Factory import create_session, check_existing_session, close_session
from classes.Auth.Token.Factory import generate_token, decode_auth_token
from classes.Auth.Token.Model import Token
from classes.Auth.PasswordHelper import Password
from fastapi import APIRouter, status, HTTPException, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth",
                   tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(new_user: NewUser):
    return create_new_user(new_user)


@router.post("/verify/{token}", status_code=status.HTTP_200_OK)
def verify_user_wtih_token(token):
    token = ObjectId(token)
    return verify_user(token)


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = get_user_by_email(form_data.username)
        if user is None:
            raise ValueError("User not found")
        if not user.is_verified:
            raise ValueError("User is not verified")
        if check_existing_session(user):
            raise ValueError(
                "Maximum number of sessions reached. Please logout from another device first.")
        if not Password.check_password(form_data.password, user.password):
            raise ValueError("Invalid email or password")
        session = create_session(
            user, request.client, request.headers.get('User-Agent'))
        if session is None:
            raise ValueError("Session not created")
        user_token = Token(user_id=user.id, session_id=session.id, token_expiration=session.token_expiration,
                           firstname=user.firstname, lastname=user.lastname, email=user.email)
        return_token = generate_token(user_token)
        return return_token
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(token: Token = Depends(decode_auth_token)):
    user = get_user_by_id(token.user_id)
    if user is None:
        raise ValueError("User not found")
    if close_session(user, token.session_id):
        return "User logged out"
    else:
        return "Session not foun"


@router.delete("/delete/session", status_code=status.HTTP_200_OK)
def delete_session(session_id, token: Token = Depends(decode_auth_token)):
    session_id = ObjectId(session_id)
    user = get_user_by_id(token.user_id)
    if user is None:
        raise ValueError("User not found")
    if close_session(user, session_id):
        return "Session deleted"
    else:
        return "Session not found"
