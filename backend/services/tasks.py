from celery import Celery
from backend.services.speech_to_text import process_audio_to_text
from backend.services.text_to_speech import generate_audio_from_text

celery_app = Celery("tasks", broker="redis://localhost:6379/0")

@celery_app.task
def async_speech_to_text(file_path: str):
    return process_audio_to_text(file_path)

@celery_app.task
def async_text_to_speech(text: str):
    output_path = f"temp/output_async.wav"
    generate_audio_from_text(text, output_path)
    return output_path