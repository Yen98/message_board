from http.client import HTTPException
from tabnanny import check
from urllib import response
from fastapi import FastAPI, HTTPException

from model import Message, User, UserOut
from database import (create_user, delete_user, find_all_user, find_message_by_author, find_message_by_author_title, password_check, post_a_message, find_all_message, user_exist, update_Message)

app = FastAPI()


@app.get('/')
async def root():
    return {"hello": "world"}

@app.get('/user/all')
async def list_all_user():
    response = await find_all_user()
    return response

@app.post('/user', response_model=UserOut)
async def create_account(user: User):
    response = await create_user(user.dict())
    if response:
        return response
    return HTTPException(400, "Something went wrong")

@app.delete('/delete/user/{username}')
async def delete_account(username: str):
    response = await delete_user(username)
    if response:
        return "Successfully deleted user"
    raise HTTPException(404, f"There is no user with the username {username}")


@app.post('/message/', response_model=Message)
async def create_message(message: Message):
    response = await post_a_message(message.dict())
    if response:
        return response
    return HTTPException(400, "Something went wrong")

@app.get('/message/all')
async def list_all_message():
    response = await find_all_message()
    return response

@app.get('/message/{author}')
async def list_message_by_author(author: str):
    response = await find_message_by_author(author)
    if response:
        return response
    raise HTTPException(404, f"There is no message by the author {author}")

@app.put('/message/update')
async def update_message(author: str, password: str, title: str, desc: str):
    d1 = await user_exist(author)
    if d1:
        d2 = await password_check(author, password)
        if d2:
            d3 = await find_message_by_author_title(author, title)
            if d3:
                response = await update_Message(author, title, desc)
                return response
            raise HTTPException(404, f"There is no message title {title} by the author {author}")
        raise HTTPException(404, f"Wrong password!!!")
    raise HTTPException(404, f"There is no author {author}")
    







