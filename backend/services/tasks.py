from celery_worker import celery_app
from  services.speech_to_text import process_audio_to_text
from servicec.text_to_speech import process_text_to_audio

@celery_app.task
def speech_to_text_task(file_path: str) -> str:
    with open(file_path, "rb") as file:
        return process_audio_to_text(file)

@celery_app.task
def text_to_speech_task(text: str) -> str:
    return process_text_to_audio(text)