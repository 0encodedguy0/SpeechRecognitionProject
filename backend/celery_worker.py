from celery import Celery

# Указываем настройки брокера для Celery
celery_app = Celery(
"tasks",
broker="redis://localhost:6379/0", # Адрес вашего Redis сервера
backend="redis://localhost:6379/0" # Адрес для сохранения результата задач
)

# Импортируем задачи, чтобы Celery знал, какие задачи обрабатывать
from backend.services.tasks import async_speech_to_text, async_text_to_speech

# Запуск воркера:
# Чтобы запустить воркер, используйте команду:
# celery -A celery_worker.celery_app worker —loglevel=info