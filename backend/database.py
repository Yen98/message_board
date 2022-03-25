from unittest import result
import motor.motor_asyncio
from model import Message, User, UserOut

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
database = client.Message_Board
user_collection = database.user
message_collection = database.message

async def find_all_user():
    users = []
    result = user_collection.find({})
    async for document in result:
        users.append(UserOut(**document))
    return users

async def create_user(user):
    document = user
    result = await user_collection.insert_one(document)
    return document

async def user_exist(user):
    document =  await user_collection.find_one({"username": user})
    return document

async def password_check(user, password):
    document  = await user_collection.find_one({"username": user, "password": password})
    return document

async def post_a_message(message):
    document = message
    result = await message_collection.insert_one(document)
    return document

async def find_all_message():
    messages = []
    result = message_collection.find({})
    async for document in result:
        messages.append(Message(**document))
    return messages

async def find_message_by_author(author):
    messages = []
    result = message_collection.find({"author": author})
    async for document in result:
        messages.append(Message(**document))
    return messages

async def find_message_by_author_title(author, title):
    document = message_collection.find_one({"author": author ,"topic": title})
    return document


async def delete_user(user):
    await user_collection.delete_one({"username": user})
    return True

async def update_Message(author, title, desc):
    old_new_messages = []
    document = await message_collection.find_one({"author": author, "topic": title})
    old_new_messages.append(Message(**document))
    await message_collection.update_one({"author": author, "topic": title}, {"$set": {"content": desc}})
    document = await message_collection.find_one({"author": author, "topic": title})
    old_new_messages.append(Message(**document))
    return old_new_messages






