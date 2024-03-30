from classes.Auth.Token.Factory import invalidated_sessions
from fastapi import APIRouter, BackgroundTasks
import asyncio
from datetime import datetime, timedelta, timezone


router = APIRouter(prefix="/cleanup", tags=["Cleanup"])
scheduled_task_handle = None


async def scheduled_task():
    # Adjust the interval as needed
    interval = timedelta(hours=5).total_seconds()
    while True:
        for session in invalidated_sessions:
            if session["expiration"] < datetime.now(timezone.utc):
                del invalidated_sessions[session]

        # Your task to be executed at a certain time interval
        print("Executing cleanup at:", datetime.now(timezone.utc))
        await asyncio.sleep(interval)  # Adjust the time interval as needed


@router.get("/start")
async def read_root(background_tasks: BackgroundTasks):
    global scheduled_task_handle
    if not scheduled_task_handle:
        scheduled_task_handle = asyncio.create_task(scheduled_task())
        return {"message": "Scheduled task started."}
    else:
        return {"message": "Scheduled task already running."}


@router.get("/stop")
async def stop_task():
    global scheduled_task_handle
    if scheduled_task_handle:
        scheduled_task_handle.cancel()
        scheduled_task_handle = None
        return {"message": "Scheduled task stopped."}
    else:
        return {"message": "No scheduled task running."}
