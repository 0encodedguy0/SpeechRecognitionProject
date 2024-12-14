from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from services.tasks import speech_to_text_task, text_to_speech_task
from celery.result import AsyncResult
from database import init_db, get_session
from models import AudioRequest, History
import logging

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/app.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS для взаимодействия с фронтендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.post("/speech-to-text/")
async def speech_to_text(file: UploadFile = File(...)):
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(await file.read())

    task = speech_to_text_task.delay(temp_file_path)
    logger.info(f"Speech-to-text task started with task_id {task.id}")
    return {"task_id": task.id}

@app.post("/text-to-speech/")
async def text_to_speech(request: AudioRequest):
    task = text_to_speech_task.delay(request.text)
    logger.info(f"Text-to-speech task started with task_id {task.id}")
    return {"task_id": task.id}

@app.get("/task-status/{task_id}/")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        return {"status": "Processing"}
    elif task_result.state == "SUCCESS":
        return {"status": "Completed", "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"status": "Failed"}
    return {"status": task_result.state}