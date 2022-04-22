from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

class Message(BaseModel):
    author: str
    content: str
    key: Optional[list] = None
    
class room(BaseModel):
    room_name: str
    users: List[User]
    messages: List[Message]

class MessageOut(BaseModel):
    author: str
    content: str

