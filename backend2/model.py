from array import array
from datetime import date
from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    userName: str
    passWord: str

class UserOut(BaseModel):
    userName: str

class Room(BaseModel):
    topic: str
    pwd: str
    creatorId: str

class RoomOut(BaseModel):
    topic: str
    creatorId: str

class Post(BaseModel):
    roomId: str
    location: int
    writtenBy: str
    content: str

class PostOut(BaseModel):
    location: int
    writtenBy: str
    content: str
    numReply: int
    reply: List

class Message(BaseModel):
    location: int
    roomId: str
    postLoc: int
    writtenBy: str
    text: str



