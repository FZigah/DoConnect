# This file contains the admin auth collection and paired profile collection
# This done to add a layer of data hiding

from pymongo import MongoClient
from dotenv import dotenv_values
import pymongo

config= dotenv_values('.env')

client = MongoClient(config['MONGO_URI'])
db = client.doconnect_db #name of db

def create_admin_auth_collection():
    try:
        db.create_collection('admin_auth')
    except Exception as e:
        return e

    db.command("collMod", "admin_auth", validator = {
        "$jsonSchema":{
        "bsonType": "object",
        "required": ["username", "password", "email"],
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "email": {
                "bsonType": "string",
                "description": "must be a string and is required",
                "pattern" : "^\\S+@\\S+\\.\\S+$"
            },
            "password": {
                "bsonType": "string",
                "minLength": 8,
                "description": "must be a string and is required"
            },
            "hashed_reset_pin":{
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "reset_expire_time":{
                "bsonType": "date",
                "description": "must be a string and is required"
            },
            "createdAt": {
                "bsonType": "date",
                "description": "must be a date and is required"
            },
            "updatedAt" : {
                "bsonType" : "date",
                "description": "must be a date and is required"
            }
        }
        }
    })


create_admin_auth_collection()
admin_auth_collection = db.admin_auth
admin_auth_collection.create_index([("email", pymongo.ASCENDING)], unique = True)

def create_admin_profile_collection():
    try:
        db.create_collection('admin_profile')
    except Exception as e:
        return e

    db.command("collMod", "admin_profile", validator = {
        "$jsonSchema":{
        "bsonType": "object",
        "required": ["username", "owner"],
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "owner": {
                "bsonType": "objectId",
                "description": "must be a string and is required",
            },
            "createdAt": {
                "bsonType": "date",
                "description": "must be a date and is required"
            },
            "updatedAt" : {
                "bsonType" : "date",
                "description": "must be a date and is required"
            }
        }
        }
    })

create_admin_profile_collection()
admin_profile_collection = db.admin_profile