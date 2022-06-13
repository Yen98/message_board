from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from database import revise_message, revise_post, find_post, find_room, delete_room, log_in_check, disjoin_a_room, show_all_user, delete_post, delete_message, get_user_name ,show_follow_room, show_all_message, show_all_post, show_all_room, join_a_room, create_a_user, create_a_post, create_a_room, create_a_message

from model import Room, Message, UserOut, User, RoomOut, Post, PostOut, MessageOut

origins = [
    "*"
]

app = FastAPI(title="Message_Board")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/show/room')
async def get_all_room():
    response = await show_all_room()
    return response

@app.get('/show/room/{userId}')
async def get_user_room(userId: str):
    response = await show_follow_room(userId)
    return response

@app.get('/show/user')
async def get_all_user():
    response = await show_all_user()
    return response

@app.get('/show/post')
async def get_all_post(roomId: str):
    response = await show_all_post(roomId)
    return response

@app.get('/show/message')
async def get_all_message(parentType: str, parentId: str):
    response = await show_all_message(parentType, parentId)
    return response

@app.get('/login')
async def login(userName: str, passWord: str):
    response = await log_in_check(userName, passWord)
    return response

@app.get('/get/userName')
async def user_name(userId: str):
    response = await get_user_name(userId)
    return response

@app.get('/find/room')
async def search_room(tag: str):
    response = await find_room(tag)
    return response

@app.get('/find/post/{roomId}')
async def search_post(roomId: str, tag: str):
    response = await find_post(roomId, tag)
    return response


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

@app.put('/disjoin')
async def disjoin_room(roomId: str, userId: str):
    response = await disjoin_a_room(roomId, userId)
    if response:
        return response
    return HTTPException(400, "Something went wrong")

@app.put('/update/post')
async def update_post(postId: str, new_content: str):
    response = await revise_post(postId, new_content)
    if response:
        return response
    return HTTPException(400, "Something went wrong")

@app.put('/update/message')
async def update_message(messageId: str, new_text: str):
    response = await revise_message(messageId, new_text)
    if response:
        return response
    return HTTPException(400, "Something went wrong")

@app.delete('/delete/room')
async def remove_room(roomId: str):
    response = await delete_room(roomId)
    if response:
        return "Successfully deleted room"
    raise HTTPException(404, f"There is no room with id {roomId}")

@app.delete('/delete/post')
async def remove_post(postId: str):
    response = await delete_post(postId)
    if response:
        return "Successfully deleted post"
    raise HTTPException(404, f"There is no post with id {postId}")

@app.delete('/delete/message')
async def remove_post(messageId: str):
    response = await delete_message(messageId)
    if response:
        return "Successfully deleted message"
    raise HTTPException(404, f"There is no message with id {messageId}")



handler = Mangum(app)