from array import array
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    userName: str
    passWord: str
    createTime: datetime

class UserOut(BaseModel):
    userName: str
    createTime: datetime

class Room(BaseModel):
    topic: str
    pwd: str
    creatorId: str
    createTime: datetime

class RoomOut(BaseModel):
    topic: str
    creatorId: str
    createTime: datetime

class Post(BaseModel):
    roomId: str
    createTime: datetime
    writtenBy: str
    content: str

class PostOut(BaseModel):
    createTime: datetime
    writtenBy: str
    content: str

class Message(BaseModel):
    parentId: str
    createTime: datetime
    writtenBy: str
    text: str

class MessageOut(BaseModel):
    createTime: datetime
    text: str


