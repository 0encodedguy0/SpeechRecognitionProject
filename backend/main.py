from fastapi import FastAPI, UploadFile, HTTPException, BackgroundTasks
from backend.services.speech_to_text import process_audio_to_text
from backend.services.text_to_speech import generate_audio_from_text
from backend.services.tasks import async_speech_to_text, async_text_to_speech

app = FastAPI(title="Speech Processing API", version="1.0.0")

@app.post("/speech-to-text/")
async def speech_to_text(file: UploadFile):
    if file.content_type != "audio/wav":
        raise HTTPException(status_code=400, detail="Только файлы WAV поддерживаются.")
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    try:
        result = process_audio_to_text(file_location)
        return {"text": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/text-to-speech/")
async def text_to_speech(background_tasks: BackgroundTasks, text: str):
    file_location = f"temp/output.wav"
    background_tasks.add_task(generate_audio_from_text, text, file_location)
    return {"message": "Аудиофайл будет готов через несколько секунд", "path": file_location}

@app.post("/tasks/speech-to-text/")
async def tasks_speech_to_text(file: UploadFile):
    if file.content_type != "audio/wav":
        raise HTTPException(status_code=400, detail="Только файлы WAV поддерживаются.")
    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())
    task_id = async_speech_to_text.delay(file_location)
    return {"task_id": task_id.id, "status": "В процессе"}

@app.post("/tasks/text-to-speech/")
async def tasks_text_to_speech(text: str):
    task_id = async_text_to_speech.delay(text)
    return {"task_id": task_id.id, "status": "В процессе"}