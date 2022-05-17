from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import log_in_check, show_all_message, show_all_post, show_all_room, join_a_room, create_a_user, create_a_post, create_a_room, get_a_room_info, create_a_message, find_message, find_message_with_tag, find_message_with_id, delete_message, delete_room

from model import Room, Message, UserOut, User, RoomOut, Post, PostOut, MessageOut

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

# @app.get('/room/{room_name}')
# async def get_room_info(room_name: str):
#     response = await get_a_room_info(room_name)
#     return response

@app.get('/show/room')
async def get_all_room():
    response = await show_all_room()
    return response

@app.get('/show/post')
async def get_all_post(roomId: str):
    response = await show_all_post(roomId)
    return response

@app.get('/show/message')
async def get_all_message(parentId: str):
    response = await show_all_message(parentId)
    return response

@app.get('/login')
async def login(userName: str, passWord: str):
    response = await log_in_check(userName, passWord)
    return response


# @app.get('/message/{room_name}')
# async def get_recent_message(room_name: str):
#     response = await find_message(room_name, 11671, 11681)
#     return response

# @app.get('/message/keyword/{room_name}')
# async def serach_message(room_name: str, keyword: str):
#     response = await find_message_with_tag(room_name, keyword)
#     return response

# @app.get('/find/{id}')
# async def get_message_by_id(id: str):
#     response = await find_message_with_id(id)
#     return response

@app.post('/user', response_model=UserOut)
async def create_account(user: User):
    response = await create_a_user(user.dict())
    if response:
        return response
    return HTTPException(400, "Something went wrong")

@app.post('/room', response_model=RoomOut)
async def create_room(room: Room):
    response = await create_a_room(room.dict())
    if response:
        return response
    return HTTPException(400, "Something went wrong")

@app.post('/post', response_model=PostOut)
async def create_post(post: Post):
    response = await create_a_post(post.dict())
    if response:
        return response
    return HTTPException(400, "Something went wrong")

@app.post('/message', response_model=MessageOut)
async def create_message(message: Message):
    response = await create_a_message(message.dict())
    if response:
        return response
    return HTTPException(400, "Something went wrong")

@app.put('/join')
async def join_room(roomId: str, userId: str):
    response = await join_a_room(roomId, userId)
    if response:
        return response
    return HTTPException(400, "Something went wrong")

# @app.delete('/delete/message/{id}')
# async def erase_message(id: str):
#     response = await delete_message(id)
#     if response:
#         return "Successfully deleted message"
#     raise HTTPException(404, f"There is no message with id {id}")

# @app.delete('/delete/room/{name}}')
# async def close_room(name: str):
#     response = await delete_room(name)
#     if response:
#         return "Successfully deleted room"
#     raise HTTPException(404, f"There is no room name {name}")
