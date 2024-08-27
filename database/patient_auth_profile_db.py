from pymongo import MongoClient
from dotenv import dotenv_values
import pymongo

config= dotenv_values('.env')

client = MongoClient(config['MONGO_URI'])
db = client.doconnect_db #name of db

def create_patient_auth_collection():
    try:
        db.create_collection('admin_auth')
    except Exception as e:
        return e

    db.command("collMod", "patient_auth", validator = {
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


create_patient_auth_collection()
patient_auth_collection = db.patient_auth
patient_auth_collection.create_index([("email", pymongo.ASCENDING)], unique = True)

def create_patient_profile_collection():
    try:
        db.create_collection('patient_profile')
    except Exception as e:
        return e

    db.command("collMod", "patient_profile", validator = {
        "$jsonSchema":{
        "bsonType": "object",
        "required": ["username", "owner", "gender", "birthdate"],
        "properties": {
            "username": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "profile_picture_url" : {
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
            "birthdate" : {
                "bsonType" : "date",
                "description" : "items must contain stated fields"
            },
             "gender": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "medicalInfo" : {
                "bsonType" : "object",
                "required" : ["bloodtype", "genotype"],
                "properties" : {
                        "bloodtype" : {
                            "bsonType" : "string",
                            "description" : "must be a string and is required"
                        },
                        "genotype" : {
                            "bsonType" : "string",
                            "description" : "must be a string"
                        }
                    }
            },
        "medicalHistory" : {
            "bsonType" : "array",
            "minItems": 1,
            "uniqueItems": True,
            "additionalProperties" : False,
            "items" : {
                "bsonType" : "object",
                "additionalProperties" : False,
                "required" : ["typeOfSickness", "period"],
                "description" : "items must contain stated fields",
                "properties" : {
                    "typeOfSickness" : {
                        "bsonType" : "string",
                        "description" : "must be a string and is required"
                    },
                    "period" : {
                        "bsonType" : "int",
                        "description" : "must be a integer and is required"
                    }
                    }
                }
        }

        }
        }
    })

create_patient_profile_collection()
patient_profile_collection = db.patient_profile