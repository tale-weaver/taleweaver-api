from pymongo import MongoClient
from dotenv import load_dotenv
import os

# import MONGO_URL from .env
load_dotenv()
URL = os.getenv("MONGO_URL")
connectionString = URL

# Create a new client and connect to the server
client = MongoClient(connectionString)
db = client["tale-weaver"]

# schema
# ref: https://www.mongodb.com/docs/manual/reference/bson-types/
if "User" not in db.list_collection_names():
    # Assuming that you want to create the "userdata" collection with a schema similar to the User class
    db.create_collection(
        "User",
        validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["username", "password", "email", "membership"],
                "properties": {
                    "username": {"bsonType": "string"},
                    "password": {"bsonType": "string"},
                    "email": {"bsonType": "string"},
                    "membership": {"bsonType": "string"},
                    "collection": {"bsonType": ["objectId"]},
                },
            }
        },
    )
    print("Created 'User' collection")
else:
    print("'User' already exists.")

if "Book" not in db.list_collection_names():
    db.create_collection(
        "Book",
        validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["bookname", "page_id", "status", "comment"],
                "properties": {
                    "bookname": {"bsonType": "string"},
                    "page_id": {"bsonType": ["objectId"]},
                    "status": {"bsonType": "string"},
                    "comment": {"bsonType": ["objectId"]},
                },
            }
        },
    )
    print("Created 'Book' collection")
else:
    print("'Book' already exists.")
if "Page.chunks" not in db.list_collection_names():
    db.create_collection(
        "Page.chunks",
        validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["files_id", "n", "data"],
                "properties": {
                    "files_id": {"bsonType": "objectId"},
                    "n": {"bsonType": "int"},
                    "data": {"bsonType": "binData"}
                }
            }
        }
    )
    print("Created 'Page.chunks' collection")
else:
    print("'Page.chunks' already exists.")

if "Page.files" not in db.list_collection_names():
    db.create_collection(
        "Page.files",
        validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": [
                    "filename",
                    "metadata",
                    "chunkSize",
                    "length",
                    "uploadDate",
                ],
                "properties": {
                    "filename": {"bsonType": "string"},
                    "metadata": {
                        "bsonType": "object",
                        "required": ["creator", "book_id", "text_description"],
                        "properties": {
                            "creator": {"bsonType": "objectId"},
                            "book_id": {"bsonType": "objectId"},
                            "text_description": {"bsonType": "string"},
                        },
                    },
                    'chunkSize': {"bsonType": "int"},
                    'length': {"bsonType": "long"},
                    'uploadDate': {"bsonType": "date"}
                },
            }
        },
    )
    print("Created 'Page.files' collection")
else:
    print("'Page.files' already exists.")
if "Comment" not in db.list_collection_names():
    db.create_collection(
        "Comment",
        validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["user_id", "content"],
                "properties": {
                    "user_id": {"bsonType": "objectId"},
                    "content": {"bsonType": "string"},
                    "comment_date": {"bsonType": "date"}
                },
            }
        },
    )
    print("Created 'Comment' collection")
else:
    print("'Comment' already exists.")

if "Page_In_Vote.chunks" not in db.list_collection_names():
    db.create_collection(
        "Page_In_Vote.chunks",
        validator = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["files_id", "n", "data"],
                "properties": {
                    "files_id": {"bsonType": "objectId"},
                    "n": {"bsonType": "int"},
                    "data": {"bsonType": "binData"}
                }
            }
        }
    )
    print("Created 'Page.chunks' collection")
else:
    print("'Page.chunks' already exists.")

if "Page_In_Vote.files" not in db.list_collection_names():
    db.create_collection(
        "Page_In_Vote.files",
        validator={
            "$jsonSchema": {
                "bsonType": "object",
                "required": [
                    "filename",
                    "metadata",
                    "chunkSize",
                    "length",
                    "uploadDate",
                ],
                "properties": {
                    "filename": {"bsonType": "string"},
                    "metadata": {
                        "bsonType": "object",
                        "required": ["creator", "book_id", "text_description", "vote"],
                        "properties": {
                            "creator": {"bsonType": "objectId"},
                            "book_id": {"bsonType": "objectId"},
                            "text_description": {"bsonType": "string"},
                            "vote": {"bsonType": "int"}
                        },
                    },
                    'chunkSize': {"bsonType": "int"},
                    'length': {"bsonType": "long"},
                    'uploadDate': {"bsonType": "date"}
                },
            }
        },
    )
    print("Created 'Page_In_Vote.files' collection")
else:
    print("'Page_In_Vote.files' already exists.")

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
