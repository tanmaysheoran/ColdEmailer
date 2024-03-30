from classes.Entities.Waitlist.Methods import insert_waitlist
from classes.Entities.Waitlist.Model import Waitlist
from pydantic import EmailStr
from fastapi import APIRouter, status, Response


router = APIRouter(prefix="/waitlist",
                   tags=["Waitlist"])


@router.get("/insert", status_code=status.HTTP_200_OK)
def add_waitlist(name: str, email: EmailStr, location: str):
    try:
        waitlist = Waitlist(name=name, email=email, location=location)
        return insert_waitlist(waitlist)
    except:
        return Response("Error occured while inserting waitlist", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
