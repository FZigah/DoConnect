from pymongo import MongoClient
from dotenv import dotenv_values
import pymongo

config= dotenv_values('.env')

client = MongoClient(config['MONGO_URI'])
db = client.doconnect_db #name of db

def create_doctor_auth_collection():
    try:
        db.create_collection('doctor_auth')
    except Exception as e:
        return e

    db.command("collMod", "doctor_auth", validator = {
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


create_doctor_auth_collection()
doctor_auth_collection = db.doctor_auth
doctor_auth_collection.create_index([("email", pymongo.ASCENDING)], unique = True)

def create_doctor_profile_collection():
    try:
        db.create_collection('doctor_profile')
    except Exception as e:
        return e

    db.command("collMod", "doctor_profile", validator = {
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
            "profile_url" : {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "status" : {
                "bsonType": "string",
                 "description": "must be a string and is required"
            },
            "experience" : {
                "bsonType": "string",
                 "description": "must be a string and is required"
            },
            "specialty" : {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "ratings_array" :{
                "bsonType" : "array",
                "minItems" : 0,
                "uniqueItems" : False,
                "items" : {
                    "bsonType" : "int",
                    "description" : "items must contain a number"
                    }
            },
            "ratings" :{
                "bsonType" : "int",
                "description": "must be a int and is required"
            },
            "contacts" : {
                "bsonType" : "array",
                "minItems": 1,
                "uniqueItems": True,
                "additionalProperties" : False,
                "items" : {
                    "bsonType" : "object",
                    "additionalProperties" : False,
                    "required" : ["contact1"],
                    "description" : "items must contain stated fields",
                    "properties" : {
                        "contact1" : {
                            "bsonType" : "string",
                            "description" : "must be a string and is required"
                        },
                        "contact2" : {
                            "bsonType" : "string",
                            "description" : "must be a string"
                        }
                    }
                }
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

create_doctor_profile_collection()
doctor_profile_collection = db.doctor_profile