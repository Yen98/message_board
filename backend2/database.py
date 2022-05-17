from model import Room, Message
import motor.motor_asyncio
from bson.objectid import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://superuser:yenbo98@localhost:27017')
database = client.TEST
user_collection = database.User
room_collection = database.Room
post_collection = database.Post
message_collection = database.Message

async def create_a_user(user):
    document = user
    document["followingRoom"] = []
    document["ownRoom"] = []
    result = await user_collection.insert_one(document)
    return user

async def create_a_room(room):
    document = room
    document["numPost"] = 0
    document["numFollower"] = 1
    result = await room_collection.insert_one(document)
    result2 = await user_collection.update_one({"_id": ObjectId(document["creatorId"])}, {"$push": {"ownRoom": str(result.inserted_id), "followingRoom": str(result.inserted_id)}})
    return room

async def create_a_post(post):
    document = post
    document["numMessage"] = 0
    result = await post_collection.insert_one(document)
    result2 = await room_collection.update_one({"_id": ObjectId(document["roomId"])}, {"$inc": {"numPost": 1}})
    return document

async def create_a_message(message):
    document = message
    document["numMessage"] = 0
    result = await message_collection.insert_one(document)
    result2 = await post_collection.update_one({"_id": ObjectId(document["parentId"])}, {"$inc": {"numMessage": 1}})
    result2 = await message_collection.update_one({"_id": ObjectId(document["parentId"])}, {"$inc": {"numMessage": 1}})
    return document

async def join_a_room(roomId, userId):
    result = await room_collection.update_one({"_id": ObjectId(roomId)}, {"$inc": {"numFollower": 1}})
    result2 = await user_collection.update_one({"_id": ObjectId(userId)}, {"$push": {"followingRoom": roomId}})
    return {"join": "success"}

async def log_in_check(userName, passWord):
    document = await user_collection.find_one({"userName": userName})
    if document:
        document = await user_collection.find_one({"userName": userName, "passWord": passWord})
        if document:
            document["_id"] = str(document["_id"])
            return document
        return {"wrong": "password"}
    return {"wrong": "username"}


async def show_all_room():
    rooms = []
    result = room_collection.find({})
    async for document in result:
        document["_id"] = str(document["_id"])
        rooms.append(document)
    return rooms

async def show_all_post(roomId):
    posts = []
    result = post_collection.find({"roomId": ObjectId(roomId)})
    async for document in result:
        document["_id"] = str(document["_id"])
        posts.append(document)
    return posts


async def show_all_message(parentId):
    messages = []
    result = message_collection.find({"parentId": ObjectId(parentId)})
    async for document in result:
        document["_id"] = str(document["_id"])
        messages.append(document)
    return messages

async def get_a_room_info(room_name):
    document = await room_collection.find_one({"topic": room_name}, {"_id": 0, "creatorId": 0})
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
