from model import Room, Message
import motor.motor_asyncio
from bson.objectid import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://yenbo98:yenbo98@cluster0.1od1a.mongodb.net/?retryWrites=true&w=majority')
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
    user["userId"] = str(result.inserted_id)
    return user

async def create_a_room(room):
    document = room
    document["numPost"] = 0
    document["numFollower"] = 1
    result = await room_collection.insert_one(document)
    result2 = await user_collection.update_one({"_id": ObjectId(document["creatorId"])}, {"$push": {"ownRoom": str(result.inserted_id), "followingRoom": str(result.inserted_id)}})
    room["roomId"] = str(result.inserted_id)
    return room

async def create_a_post(post):
    document = post
    document["numMessage"] = 0
    result = await post_collection.insert_one(document)
    result2 = await room_collection.update_one({"_id": ObjectId(document["roomId"])}, {"$inc": {"numPost": 1}})
    post["postId"] = str(result.inserted_id)
    return post

async def create_a_message(message):
    document = message
    document["numMessage"] = 0
    result = await message_collection.insert_one(document)
    if document["parentType"] == "post":
        result2 = await post_collection.update_one({"_id": ObjectId(document["parentId"])}, {"$inc": {"numMessage": 1}})
    elif document["parentType"] == "message":
        result2 = await message_collection.update_one({"_id": ObjectId(document["parentId"])}, {"$inc": {"numMessage": 1}})
    message["messageId"] = str(result.inserted_id)
    return document

async def join_a_room(roomId, userId):
    result = await room_collection.update_one({"_id": ObjectId(roomId)}, {"$inc": {"numFollower": 1}})
    result2 = await user_collection.update_one({"_id": ObjectId(userId)}, {"$push": {"followingRoom": roomId}})
    return {"join": "success"}

async def disjoin_a_room(roomId, userId):
    result = await room_collection.update_one({"_id": ObjectId(roomId)}, {"$inc": {"numFollower": -1}})
    result2 = await user_collection.update_one({"_id": ObjectId(userId)}, {"$pull": {"followingRoom": roomId, "ownRoom": roomId}})
    return {"disjoin": "success"}

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

async def show_follow_room(userId):
    rooms = []
    result = await user_collection.find_one({"_id": ObjectId(userId)}, {"_id": 0, "followingRoom": 1})
    for roomId in result["followingRoom"]:
        document = await room_collection.find_one({"_id": ObjectId(roomId)})
        document["_id"] = str(document["_id"])
        rooms.append(document)
    return rooms

async def show_all_user():
    users = []
    result = user_collection.find({})
    async for document in result:
        document["_id"] = str(document["_id"])
        users.append(document)
    return users

async def show_all_post(roomId):
    posts = []
    result = post_collection.find({"roomId": roomId})
    async for document in result:
        document["_id"] = str(document["_id"])
        posts.append(document)
    return posts


async def show_all_message(parentType, parentId):
    messages = []
    result = message_collection.find({"parentType": parentType, "parentId": parentId})
    async for document in result:
        document["_id"] = str(document["_id"])
        messages.append(document)
    return messages


async def delete_room(roomId):
    room = await room_collection.find_one({"_id": ObjectId(roomId)})
    result = await room_collection.update_one({"_id": ObjectId(post["roomId"])}, {"$inc": {"numPost": -1}})
    result2 = message_collection.find({"parentType": "post", "parentId": postId}, {"_id": 1})
    async for document in result2:
        await delete_message(str(document["_id"]))
    await post_collection.delete_one({"_id": ObjectId(postId)})
    return True

async def delete_message(messageId):
    message = await message_collection.find_one({"_id": ObjectId(messageId)})
    if message["parentType"] == "post":
        result = await post_collection.update_one({"_id": ObjectId(message["parentId"])}, {"$inc": {"numMessage": -1}})
    elif message["parentType"] == "message":
        result = await message_collection.update_one({"_id": ObjectId(message["parentId"])}, {"$inc": {"numMessage": -1}})
    result2 = message_collection.find({"parentType": "message", "parentId": messageId}, {"_id": 1})
    async for document in result2:
        await delete_message(str(document["_id"]))
    await message_collection.delete_one({"_id": ObjectId(messageId)})
    return True

async def delete_post(postId):
    post = await post_collection.find_one({"_id": ObjectId(postId)})
    result = await room_collection.update_one({"_id": ObjectId(post["roomId"])}, {"$inc": {"numPost": -1}})
    result2 = message_collection.find({"parentType": "post", "parentId": postId}, {"_id": 1})
    async for document in result2:
        await delete_message(str(document["_id"]))
    await post_collection.delete_one({"_id": ObjectId(postId)})
    return True

async def delete_room(roomId):
    room = await room_collection.find_one({"_id": ObjectId(roomId)})
    result = await user_collection.update_one({"_id": ObjectId(room["creatorId"])}, {"$pull": {"followingRoom": roomId, "ownRoom": roomId}})
    result2 = post_collection.find({"roomId": roomId}, {"_id": 1})
    async for document in result2:
        await delete_post(str(document["_id"]))
    await room_collection.delete_one({"_id": ObjectId(roomId)})
    return True


async def get_user_name(userId):
    user = await user_collection.find_one({"_id": ObjectId(userId)}, {"_id": 0, "userName": 1})
    return user

async def find_room(tag):
    rooms = []
    result = room_collection.find({"topic": {"$regex": tag}})
    async for document in result:
        document["_id"] = str(document["_id"])
        rooms.append(document)
    return rooms

async def find_post(roomId, tag):
    posts = []
    result = post_collection.find({"roomId": roomId, "content": {"$regex": tag}})
    async for document in result:
        document["_id"] = str(document["_id"])
        posts.append(document)
    return posts

async def revise_post(postId, new_content):
    await post_collection.update_one({"_id": ObjectId(postId)}, {"$set": {"content": new_content}})
    return {"update": "success"}

async def revise_message(messageId, new_text):
    await message_collection.update_one({"_id": ObjectId(messageId)}, {"$set": {"text": new_text}})
    return {"update": "success"}


