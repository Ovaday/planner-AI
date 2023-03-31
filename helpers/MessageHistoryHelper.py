import pymongo
from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE_USER_NAME = os.environ.get("DATABASE_USER_NAME")
DATABASE_USER_PASSWORD = os.environ.get("DATABASE_USER_PASSWORD")

client = pymongo.MongoClient("mongodb+srv://"+DATABASE_USER_NAME+":"+DATABASE_USER_PASSWORD+"@planneraidev.efkepet.mongodb.net/?retryWrites=true&w=majority")

db = client["messages-database"]

col = db["messages"]

message = {
    "ChatId": 0,
    "MessageTime": datetime.now(),
    "MessageId": 0,
    "isResponse": False,
    "Username": "Alexandr",
    "ExternalId": "",
    "AdditionalInfo": {
        "field": "fieldValue"
    },
    "Message": "some text",
    "Message encrypted": 0b100000
}

col.insert_one(message)

for x in col.find({},{ "ChatId": 0}):
    print(x)



