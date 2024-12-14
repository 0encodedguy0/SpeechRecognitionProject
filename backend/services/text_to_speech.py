from gtts import gTTS

def generate_audio_from_text(text: str, output_path: str):
    tts = gTTS(text, lang="ru")
    tts.save(output_path)