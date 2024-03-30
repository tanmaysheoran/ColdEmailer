from classes.Entities.User.Factory import get_user_by_id
from classes.Auth.Token.Factory import decode_auth_token
from classes.Entities.User.Methods import upload_file, update_by_id, get_file_list, get_file_bytes_by_id
from classes.Entities.Person.Factory import get_person_with_company_name_by_id
from classes.Entities.Prompts.Factory import get_prompt_by_id
from classes.Entities.UserEmailTemplate.Factory import generate_and_store_email_template
from classes.Entities.UserEmailTemplate.Methods import send_email_template, update_email_template
from classes.Google.Auth import Auth as GoogleAuth
from classes.Auth.Token.Model import Token
from classes.Entities.Task.Model import Task
from classes.Entities.Task.Methods import save as save_task
from fastapi import APIRouter, status, Depends, File, UploadFile, BackgroundTasks, Response
from bson import ObjectId


router = APIRouter(prefix="/user",
                   tags=["User"], dependencies=[Depends(decode_auth_token)])


@router.get("/me", status_code=status.HTTP_200_OK)
def me(decoded_token: Token = Depends(decode_auth_token)):
    return get_user_by_id(decoded_token.user_id)


@router.post("/profile/upload/file", status_code=status.HTTP_201_CREATED)
def upload_file(file: UploadFile = File(...), tags=str, decoded_token: Token = Depends(decode_auth_token)):
    file_id = upload_file(file.file.read(), file.filename,
                          decoded_token.user_id, tags=tags.split(","))
    return {"filename": file.filename, "file_id": str(file_id)}


@router.post("/profile/upload/image", status_code=status.HTTP_201_CREATED)
def upload_image(file: UploadFile = File(...), decoded_token: Token = Depends(decode_auth_token)):
    file_id = upload_file(file.file.read(), "profile_image.jpg",
                          decoded_token.user_id, tags=["profile_image"])
    update_by_id(decoded_token.user_id, {"imageId": file_id})
    return {"filename": file.filename}


@router.get("/profile/files", status_code=status.HTTP_200_OK)
def get_files_list(tags: str, decoded_token: Token = Depends(decode_auth_token)):
    files = get_file_list(decoded_token.user_id, tags=tags.split(","))
    files = [item.model_dump(mode="json") for item in files]
    return files


@router.get("/profile/email_template/create", status_code=status.HTTP_202_ACCEPTED)
def create_template(file_id: str, person_id: str, prompt_id: str, background_tasks: BackgroundTasks, decoded_token: Token = Depends(decode_auth_token)):
    user = get_user_by_id(decoded_token.user_id)
    person_and_company = get_person_with_company_name_by_id(
        ObjectId(person_id))
    if not person_and_company:
        return Response("Person not found", status_code=204)
    person, company_name = person_and_company

    file = get_file_bytes_by_id(file_id)
    if not file:
        return Response("File not found", status_code=204)

    prompt = get_prompt_by_id(prompt_id)
    if not prompt:
        return Response("Prompt not found", status_code=204)
    input_text = f"{person.first_name} {person.last_name}"
    task = Task(method="Email Template", input=input_text)
    save_task(task)
    background_tasks.add_task(
        generate_and_store_email_template, file, prompt, person, user, company_name, task)
    return Response({"id": str(task.id), "status": task.status}, status_code=202)


@router.post("/profile/email_template/send", status_code=status.HTTP_200_OK)
def send_email(email_template_id: str, decoded_token: Token = Depends(decode_auth_token)):
    return_response_type = "text/html"
    user = get_user_by_id(decoded_token.user_id)
    google_auth = GoogleAuth()
    user_crendentials = google_auth.get_user_credentials(user_id=user.id)
    if not user_crendentials:
        return Response("User Credentials not found", status_code=204, media_type=return_response_type)
    email_template = [
        template for template in user.email_templates if template.id == ObjectId(email_template_id)]
    if not email_template:
        return Response("Email Template not found", status_code=204, media_type=return_response_type)
    email_template = email_template[0]
    if email_template.sent:
        return Response("Email already sent", status_code=200, media_type=return_response_type)
    email_sent = send_email_template(email_template, user_crendentials, user)
    if email_sent:
        return Response("Email Sent", status_code=200, media_type=return_response_type)
    else:
        return Response("Email Failed", status_code=500, media_type=return_response_type)


@router.put("/profile/email_template/update", status_code=status.HTTP_200_OK)
def update_user_email_template(email_template_properties: dict, email_template_id: str, decoded_token: Token = Depends(decode_auth_token)):

    try:
        updated = update_email_template(
            email_template_properties, decoded_token.user_id, ObjectId(email_template_id))
        if not updated:
            return Response("Email Template Update Failed", status_code=500, media_type="text/html")

        return Response("Email Template Updated", status_code=200, media_type="text/html")
    except Exception as e:
        return Response(str(e), status_code=500)
