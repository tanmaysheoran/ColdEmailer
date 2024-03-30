from classes.Entities.Prompts.Factory import get_promt_by_tag
from classes.Auth.Token.Factory import decode_auth_token
from fastapi import APIRouter, status, Depends

router = APIRouter(prefix="/prompt",
                   tags=["Prompt"], dependencies=[Depends(decode_auth_token)])


@router.get("/get_by_tag", status_code=status.HTTP_200_OK)
def get_prompt_list_by_tags(tags: str):
    return get_promt_by_tag(tags.split(","))
