from classes.Auth.Token.Factory import decode_auth_token
from classes.Google.Maps import Maps
from fastapi import APIRouter, status
from fastapi import Depends

router = APIRouter(prefix="/location",
                   tags=["Location"])
# , dependencies=[Depends(decode_auth_token)])


@router.get("/autocomplete", status_code=status.HTTP_200_OK)
def autocomplete_location(location: str):
    return Maps().autocomplete(location)
