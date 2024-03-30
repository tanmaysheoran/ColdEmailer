from classes.Search.LinkedInSearch import LinkedInSearch
from classes.Auth.Token.Factory import decode_auth_token
from classes.Google.Search.CustomSearch import GoogleCustomSearch
from classes.Entities.Company.Factory import get_company_by_id, get_all_companies
from classes.Entities.Company.Methods import lookup
from classes.Entities.Task.Model import Task
from classes.Entities.Task.Methods import save as save_task
from fastapi import BackgroundTasks, status, Query
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/company",
                   tags=["Company"], dependencies=[Depends(decode_auth_token)])

google_custom_search = GoogleCustomSearch()


@router.get("/linkedin_search", status_code=status.HTTP_202_ACCEPTED)
def linedin_search(role: str, company: str, location: str, background_tasks: BackgroundTasks, pages: int = Query(1, ge=1, le=10), company_uuid: str = None):
    input_text = f"{role} - {company} - {location}"
    task = Task(method="LinkedInSearch", input=input_text)
    task_id = save_task(task)
    linkedin_search = LinkedInSearch(
        role, company, location, pages, task, company_uuid)
    background_tasks.add_task(linkedin_search.process)
    return {"id": str(task.id), "status": task.status}


@router.get("/all", status_code=status.HTTP_200_OK)
def get_all(pages: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    result = get_all_companies(pages, limit)
    return result


@router.get("/by_id/{id}", status_code=status.HTTP_200_OK)
def get_company_info(id: str):
    result = get_company_by_id(id)
    return result


@router.get("/autocomplete", status_code=status.HTTP_200_OK)
def autocomplete_company(company_name: str):
    result = lookup(company_name)
    return result
