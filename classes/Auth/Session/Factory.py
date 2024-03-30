from classes.Auth.Session.Model import Session
from classes.Auth.User.Model import AuthUser
from classes.Auth.User.Methods import update
from bson import ObjectId
from datetime import datetime, timezone, timedelta
import os

allowed_sessions = 5
invalidated_sessions = {}
token_expiration = timedelta(hours=os.environ.get("TOKEN_EXPIRATION") or 8)


def check_existing_session(user: AuthUser):
    return not len(user.active_sessions) < allowed_sessions


def create_session(user: AuthUser, ip_address: str, user_agent: str) -> Session:
    session = Session(
        id=ObjectId(),
        ip_address=ip_address,
        user_agent=user_agent,
        login_time=datetime.now(timezone.utc),
        logout_time=None,
        token_expiration=datetime.now(timezone.utc) + token_expiration
    )
    user.active_sessions.append(session)
    if update(user):
        return session
    else:
        raise Exception("Error occurred while creating session")


def close_session(user: AuthUser, session_id: ObjectId) -> Session:
    session = [item for item in user.active_sessions if item.id == session_id]
    if session:
        session = session[0]
        user.active_sessions.remove(session)
        session.logout_time = datetime.now(timezone.utc)
        user.inactive_sessions.append(session)
        invalidated_sessions[session_id] = session.token_expiration
        updated = update(user)
        return updated
    return False
