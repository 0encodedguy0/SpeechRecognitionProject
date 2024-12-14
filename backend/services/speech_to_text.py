from vosk import Model, KaldiRecognizer
import wave
import os

MODEL_PATH = "models/vosk-model-small-ru-0.22"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Модель не найдена по пути {MODEL_PATH}."
)

def process_audio_to_text(file_path: str) -> str:
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    with wave.open(file_path, "rb") as audio_file:
        if audio_file.getnchannels() != 1 or audio_file.getsampwidth() != 2 or audio_file.getframerate() != 16000:
            raise ValueError("Файл должен быть моно, 16-битный, 16000 Гц")
        data = audio_file.readframes(audio_file.getnframes())
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            return eval(result)["text"]

    return "Не удалось распознать речь"
