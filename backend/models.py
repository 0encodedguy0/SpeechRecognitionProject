from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel

class History(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str
    input: str
    output: str

class AudioRequest(BaseModel):
    text: str