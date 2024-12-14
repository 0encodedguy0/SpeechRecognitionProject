from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class AudioRequest(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    text: str
    file_path: str

class TextToSpeechRequest(BaseModel):
    text: str