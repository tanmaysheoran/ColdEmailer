from bson import ObjectId
from fastapi import APIRouter, status, HTTPException, Depends
from pydantic import HttpUrl
from fastapi.responses import HTMLResponse
from classes.Auth.Token.Factory import decode_auth_token
from classes.Auth.User.Factory import get_user_by_id
from classes.Auth.Token.Model import Token
from classes.Google.Auth import Auth as GoogleAuth

router = APIRouter(prefix="/auth/google", tags=["Google Auth", "Auth"])


@router.get("/auth_url", status_code=status.HTTP_200_OK)
def get_auth_url(redirect_url: HttpUrl, token: Token = Depends(decode_auth_token)) -> HTMLResponse:
    """
    Generate Google authentication URL.
    """
    state = {"user_id": str(token.user_id), "redirect_url": str(redirect_url)}
    auth = GoogleAuth(state)
    auth_url = auth.get_auth_url()
    return HTMLResponse(content=f'<script>window.location.href="{auth_url}"</script>', media_type="text/html")


@router.get("/callback", status_code=status.HTTP_200_OK)
def callback(state: str, code: str) -> HTMLResponse:
    """
    Handle Google authentication callback.
    """
    try:
        auth = GoogleAuth(encoded_state=state)
        credentials = auth.get_credentials_json(code)
        auth_user = get_user_by_id(ObjectId(auth.state["user_id"]))
        redirect_url = auth.state["redirect_url"]

        if auth.save_credentials(credentials, auth_user):
            return HTMLResponse(content=f'<script>window.location.href="{redirect_url}"</script>', media_type="text/html")
        else:
            return HTMLResponse(content='<script>window.close()</script>', media_type="text/html")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return HTMLResponse(content='<script>window.close()</script>', media_type="text/html")


@router.get("/user/validate_credentials", status_code=status.HTTP_200_OK)
def validate_credentials(token: Token = Depends(decode_auth_token)) -> bool:
    """
    Validate user credentials.
    """
    user = get_user_by_id(token.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    auth = GoogleAuth()
    return auth.validate_credentials(user)
