import os

import minecraftapi
import pymongo
from bson.binary import JAVA_LEGACY
from bson.codec_options import CodecOptions
from dotenv import load_dotenv

load_dotenv()

mongoClient = pymongo.MongoClient(os.environ["MONGODB_CONNECTION_STRING"])
db = mongoClient["main"]
collection = db.get_collection("users", CodecOptions(uuid_representation=JAVA_LEGACY))


def is_uuid_registred(uuid) -> bool:
    found = collection.find_one({
        "uuid": uuid
    })
    return found is not None


def is_username_registred(username: str) -> bool:
    return is_uuid_registred(minecraftapi.get_uuid(username))


def register_uuid(uuid, discord_userid: int):
    if is_uuid_registred(uuid):
        return
    document = {
        "uuid": uuid,
        "can_access": True,
        "discord": discord_userid
    }
    collection.insert_one(document)


def register_user(username: str, discord_userid: int):
    register_uuid(minecraftapi.get_uuid(username), discord_userid)


def is_discord_user_registred(discord_userid: int) -> bool:
    found = collection.find_one({
        "discord": discord_userid
    })
    return found is not None
