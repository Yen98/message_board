from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import find_all_message, create_a_room, get_a_room_info, write_a_message, find_message, find_message_with_tag, find_message_with_id, delete_message, delete_room

from model import Room, Message, Messages

origins = [
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/room/{room_name}')
async def get_room_info(room_name: str):
    response = await get_a_room_info(room_name)
    return response

@app.get('/message/{room_name}')
async def get_recent_message(room_name: str):
    response = await find_message(room_name, 11671, 11681)
    return response

@app.get('/message/keyword/{room_name}')
async def serach_message(room_name: str, keyword: str):
    response = await find_message_with_tag(room_name, keyword)
    return response

@app.get('/find/{id}')
async def get_message_by_id(id: str):
    response = await find_message_with_id(id)
    return response

@app.post('/room', response_model=Room)
async def create_room(room: Room):
    response = await create_a_room(room.dict())
    if response:
        return response
    return HTTPException(400, "Something went wrong")

@app.post('/message', response_model=Message)
async def create_a_message(message: Message):
    response = await write_a_message(message.dict())
    if response:
        return response
    return HTTPException(400, "Something went wrong")

@app.post('/many_message')
async def create_many_message(message: Messages):
    for m in message.message:
        response = await write_a_message(m.dict())
    if response:
        return {"haha"}
    return HTTPException(400, "Something went wrong")

@app.delete('/delete/message/{id}')
async def erase_message(id: str):
    response = await delete_message(id)
    if response:
        return "Successfully deleted message"
    raise HTTPException(404, f"There is no message with id {id}")

@app.delete('/delete/room/{name}}')
async def close_room(name: str):
    response = await delete_room(name)
    if response:
        return "Successfully deleted room"
    raise HTTPException(404, f"There is no room name {name}")

@app.get('/all_message')
async def get_all_messages():
    response = await find_all_message()
    return response

