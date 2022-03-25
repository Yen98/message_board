from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

class Message(BaseModel):
    author: str
    topic: str
    content: str
