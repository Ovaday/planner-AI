import pymongo
from datetime import datetime
from tokenHelpers import get_token

DATABASE_USER_NAME = get_token("DATABASE_USER_NAME")
DATABASE_USER_PASSWORD = get_token("DATABASE_USER_PASSWORD")
DATABASE_ENVIROMENT = get_token("DATABASE_ENVIROMENT")

client = pymongo.MongoClient("mongodb+srv://"+DATABASE_USER_NAME+":"+DATABASE_USER_PASSWORD+"@"+DATABASE_ENVIROMENT+"/?retryWrites=true&w=majority")

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



