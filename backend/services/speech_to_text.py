from vosk import Model, KaldiRecognizer
import wave
import os

# Указываем путь к русской модели
MODEL_PATH = "models/vosk-model-small-ru-0.22"

# Проверяем, существует ли модель
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Модель не найдена по пути {MODEL_PATH}."
    )

# Функция для обработки аудио в текст
def process_audio_to_text(file_path: str) -> str:
    # Загружаем модель
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    # Открываем WAV-файл
    with wave.open(file_path, "rb") as audio_file:
        if audio_file.getnchannels() != 1 or audio_file.getsampwidth() != 2 or audio_file.getframerate() != 16000:
            raise ValueError("Файл должен быть моно, 16-битный, 16000 Гц")

        # Считываем данные и выполняем распознавание
        data = audio_file.readframes(audio_file.getnframes())
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            return eval(result)["text"] # Преобразуем строку результата в словарь и извлекаем текст

        return "Не удалось распознать речь"