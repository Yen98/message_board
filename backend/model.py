from pickle import NONE
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

class Message(BaseModel):
    author: str
    topic: str
    content: str
    key: Optional[list] = None

class MessageOut(BaseModel):
    author: str
    topic: str
    content: str

