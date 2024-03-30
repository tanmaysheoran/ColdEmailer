from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from classes.Entities.Task.Factory import get_task_by_id
import asyncio

router = APIRouter(prefix="/task", tags=["Task"])


@router.websocket("/status/{task_id}")
async def get_task_status(websocket: WebSocket, task_id: str):
    try:
        await websocket.accept()
        while True:
            task = get_task_by_id(task_id)
            await websocket.send_text(task.status)
            if task.status.lower() in ["completed", "failed"]:
                break
            await asyncio.sleep(1)  # Adjust the sleep time as needed
    except WebSocketDisconnect:
        # Handle WebSocket disconnection
        pass
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {str(e)}")
    finally:
        await websocket.close()
