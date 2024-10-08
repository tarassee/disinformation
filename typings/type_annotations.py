from typing import Optional
from pydantic import BaseModel


class Request(BaseModel):
    content: str


class RedFlag(BaseModel):
    RedFlagId: int
    Phrase: str
    Description: Optional[str] = None
