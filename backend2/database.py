from model import Room, Message
import motor.motor_asyncio
import re

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/')
database = client.Chat_Room
room_collection = database.room
message_collection = database.message

async def create_a_room(room):
    document = room
    document["number_of_messages"] = 0
    document["conversation"] = []
    result = await room_collection.insert_one(document)
    return document

async def get_a_room_info(room_name):
    document = await room_collection.find_one({"name": room_name}, {"_id": 0, "name": 1, "key": 1, "users": 1, "number_of_messages": 1})
    return document

async def write_a_message(message):
    document = message
    document["tag"] = re.split(',[ ]*|[ ]+|\.[ ]*|\(|\)|[!?;][ ]*', document["content"])
    result = await message_collection.insert_one(document)
    result2 = await room_collection.update_one({"name": document["room_name"]}, {"$inc": {"number_of_messages": 1}})
    result3 = await room_collection.update_one({"name": document["room_name"]}, {"$push": {"conversation": result.inserted_id}})
    return message

async def find_message(room_name, begin, end):
    messages = []
    room = await room_collection.find_one({"name": room_name})
    for i in range(begin, end):
        document = await message_collection.find_one({"_id": room["conversation"][i]}, {"_id": 0})
        document.pop("tag")
        messages.append(document)
    return messages

async def find_message_with_tag(room_name, tag):
    messages = []
    # result = message_collection.find({"room_name": room_name, "tag": tag}, {"_id": 0}).limit(50)
    result = message_collection.find( { "$text": { "$search": tag }}, {"_id": 0, "tag": 0} ).limit(50)
    async for document in result:
        messages.append(document)
    return messages


    
    
    
        
    
    
