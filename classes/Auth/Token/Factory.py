from classes.Auth.Token.Model import Token, JWT
from classes.Auth.Session.Factory import invalidated_sessions
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
import os
import jwt


token_secret = os.environ.get("TOKEN_SECRET")
oauth2_scheme = HTTPBearer()


def generate_token(token: Token) -> JWT:
    access_token = jwt.encode(
        token.model_dump(mode='json'), token_secret, algorithm='HS256')
    token_type = "Bearer"
    return JWT(access_token=access_token, token_type=token_type)


def decode_token(token: str) -> Token:
    try:
        payload = jwt.decode(token, token_secret,
                             algorithms=['HS256'])
        payload["id"] = ObjectId(payload["id"])
        payload['session_id'] = ObjectId(payload['session_id'])
        payload['user_id'] = ObjectId(payload['user_id'])
        return Token(**payload)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


async def decode_auth_token(token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]) -> Token:
    decoded_token = decode_token(token.credentials)
    if decoded_token is None:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid token")
    if decoded_token.session_id in invalidated_sessions:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Session expired")
    return decoded_token
