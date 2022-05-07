from array import array
from typing import List
from model import Room, Message
import motor.motor_asyncio
import re
from bson.objectid import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://superuser:yenbo98@localhost:27017')
database = client.TEST
room_collection = database.Room
post_collection = database.Post
message_collection = database.message
user_collection = database.User

async def create_a_room(room):
    document = room
    document["creatorId"] = ObjectId(document["creatorId"])
    document["follower"] = []
    document["numPost"] = 0
    document["post"]= []
    result = await room_collection.insert_one(document)
    document["creatorId"] = str(document["creatorId"])
    return room

async def create_a_user(user):
    document = user
    document["followingRoom"] = []
    document["ownRoom"] = []
    result = await user_collection.insert_one(document)
    return document

async def create_a_post(post):
    document = post
    roomId = ObjectId(document["roomId"])
    document["writtenBy"] = ObjectId(document["writtenBy"])
    document["numReply"] = 0
    document["reply"] = []
    document.pop("roomId")
    result = await room_collection.update_one({"_id": roomId}, {"$inc": {"numPost": 1}, "$push": {"post": document}})
    document["writtenBy"] = str(document["writtenBy"])
    return document

async def create_a_message(message):
    document = message
    roomId = ObjectId(document["roomId"])
    document.pop("roomId")
    document["writtenBy"] = ObjectId(document["writtenBy"])
    document["reply"] = []
    result = await room_collection.update_one({"_id": roomId}, {"$inc": {"numPost": 1}, "$push": {"post": document}})
    document["writtenBy"] = str(document["writtenBy"])
    return document


async def find_all_message():
    messages = []
    result = message_collection.find({})
    async for document in result:
        document["_id"] = str(document["_id"])
        messages.append(document)
    return messages


async def get_a_room_info(room_name):
    document = await room_collection.find_one({"name": room_name}, {"_id": 0, "name": 1, "key": 1, "users": 1, "number_of_messages": 1})
    return document


async def find_message(room_name, begin, end):
    messages = []
    room = await room_collection.find_one({"name": room_name})
    for i in range(begin, end):
        document = await message_collection.find_one({"_id": room["conversation"][i]}, {"_id": 0})
        messages.append(document)
    return messages

async def find_message_with_tag(room_name, tag):
    messages = []
    #result = message_collection.find( { "$text": { "$search": tag }}, {"_id": 0} ).limit(50)
    result = message_collection.find({"content": {"$regex": tag }}).limit(50)
    async for document in result:
        document["_id"] = str(document["_id"])
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