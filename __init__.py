from classes.Database.MongoDBManager import MongoDBCollectionManager
from routes.Company import router as company
from routes.Task import router as task
from routes.Location import router as location
from routes.Cleanup import router as cleanup
from routes.Auth import router as auth
from routes.User import router as user
from routes.Prompt import router as prompt
from routes.GoogleAuth import router as google_auth
from routes.Waitlist import router as waitlist
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
import time

collections_to_iniliaze = ["Users", "Companies", "Tasks"]
MongoDBCollectionManager().create_collections(collections_to_iniliaze)
app = FastAPI(title="thehightabl.api", name="thehightabl.api", version="beta")
api_v1 = "/api/v1"

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth, prefix=api_v1)
app.include_router(company, prefix=api_v1)
app.include_router(task, prefix=api_v1)
app.include_router(location, prefix=api_v1)
app.include_router(cleanup, prefix=api_v1)
app.include_router(user, prefix=api_v1)
app.include_router(prompt, prefix=api_v1)
app.include_router(google_auth, prefix=api_v1)
app.include_router(waitlist, prefix=api_v1)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
