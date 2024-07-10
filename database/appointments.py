from pymongo import MongoClient
from dotenv import dotenv_values
import pymongo

config= dotenv_values('.env')

client = MongoClient(config['MONGO_URI'])
db = client.doconnect_db #name of db


def create_appointments_collection():
    try:
        db.create_collection('appointments')
    except Exception as e:
        return e

    db.command("collMod", "appointments", validator = {
        "$jsonSchema":{
        "bsonType": "object",
        "required": ["patient_name", "patient_description", "patient_id", "patient_profile_picture_url", "doctor_id", "doctor_name" ],
        "properties": {
            "patient_name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "patient_description": {
                "bsonType": "string",
                "description": "must be a string and is required",
            },
            "patient_id": {
                "bsonType": "objectId",
                "description": "must be a string and is required"
            },
             "patient_profile_picture_url": {
                "bsonType": "string",
                "description": "must be a date and is required"
            },
            "doctor_id": {
                "bsonType": "objectId",
                "description": "must be a string and is required"
            },
            "doctor_name": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "appointment_status": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
             "appointment_date": {
                "bsonType": "date",
                "description": "must be a date and is required"
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


create_appointments_collection()
appointments_collection = db.appointments


