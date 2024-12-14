from celery import Celery

# Конфигурация
celery_app = Celery(
    "tasks",
    brocker="redis://localhost:6379/0",  # Redis как брокер задач
    backend="redis://localhost:6379/1",  # Redis как хранилище результатов
)

celery_app.conf.task_routes = {
    "tasks.speech_to_text": {"queue": "speech"},
    "tasks.text_to_speech": {"queue": "speech"},
}