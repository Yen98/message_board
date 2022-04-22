from array import array
from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    name: str
    password: str

class Message(BaseModel):
    room_name: str
    writtenby: str
    content: str

class Messages(BaseModel):
    message: List[Message]

class Room(BaseModel):
    name: str
    key: str
    users: List[str]

