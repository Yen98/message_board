from array import array
from typing import List
from model import Room, Message
import motor.motor_asyncio
import re
from bson.objectid import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://yenbo98:yenbo98@cluster0.1od1a.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
database = client.Chat_Room
room_collection = database.room
message_collection = database.message
user_collection = database.user

async def create_a_room(room):
    document = room
    document["number_of_messages"] = 0
    document["conversation"] = []
    result = await room_collection.insert_one(document)
    return document

async def find_all_message():
    messages = []
    result = room_collection.find({}, {"conversation": 0})
    async for document in result:
        document["_id"] = str(document["_id"])
        messages.append(document)
    return messages


async def get_a_room_info(room_name):
    document = await room_collection.find_one({"name": room_name}, {"_id": 0, "name": 1, "key": 1, "users": 1, "number_of_messages": 1})
    return document

async def write_a_message(message):
    document = message
    result = await message_collection.insert_one(document)
    result2 = await room_collection.update_one({"name": document["room_name"]}, {"$inc": {"number_of_messages": 1}, "$push": {"conversation": result.inserted_id}})
    return message

async def find_message(room_name, begin, end):
    messages = []
    room = await room_collection.find_one({"name": room_name})
    for i in range(begin, end):
        document = await message_collection.find_one({"_id": room["conversation"][i]}, {"_id": 0})
        messages.append(document)
    return messages

async def find_message_with_tag(room_name, tag):
    messages = []
    result = message_collection.find( { "$text": { "$search": tag }}, {"_id": 0} ).limit(50)
    async for document in result:
        messages.append(document)
    return messages

async def find_message_with_id(id):
    document = await message_collection.find_one({"_id": ObjectId(id)}, {"_id": 0})
    return document

async def delete_message(id):
    result = await room_collection.update_one({"conversation": ObjectId(id)}, {"$inc": {"number_of_messages": -1}, "$pull": {"conversation": ObjectId(id)}})
    await message_collection.delete_one({"_id": ObjectId(id)})
    return True

async def delete_room(name):
    await room_collection.delete_one({"name": name})
    await message_collection.delete_many({"room_name": name})
    return True