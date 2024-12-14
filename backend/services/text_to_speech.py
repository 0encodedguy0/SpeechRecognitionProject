from gtts import gTTS
import os

def process_text_to_audio(text: str) -> str:
    file_path = f"output_{hash(text)}.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(file_path)
    return file_path