from fastapi import BackgroundTasks
from services.tasks import speech_to_text_task, text_to_speech_task
from celery.result import AsyncResult

@app.post("/speech-to-text/")
async def speech_to_text(file: UploadFile = File(...), background_tasks: BackgroundTasks):
    # Сохранение файла временно
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(await file.read())

    # Запуск фоновой задачи
    task = speech_to_text_task.delay(temp_file_path)
    return {"task_id": task.id}

@app.post("/text-to-speech/")
async def text_to_speech(request: AudioRequest):
    task = text_to_speech_task.delay(request.text)
    return {"task_id": task.id}

@app.get("/task-status/{task_id}/")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == "PENDING":
        return {"status": "Processing"}
    elif task_result.state == "SUCCESS":
        return {"status": "Completed", "result": task_result.result}
    else:
        return {"status": task_result.state}