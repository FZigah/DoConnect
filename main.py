from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routers.admin import admin_auth,admin_ctrl
from routers.doctor import doctor_auth, doctor_ctrl
from routers.patient import patient_auth, patient_ctrl
from fastapi.middleware.cors import CORSMiddleware
app= FastAPI()

# config = dotenv_values(".env")
# client = MongoClient(config["MONGO_URI"])
# try:
#     client.admin.command("ping")
#     print("successfully connected to mongo")
# except Exception as e:
#     print(e)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def homepage():
    return 'Welcome to DoConnect'

app.include_router(admin_auth.router)
app.include_router(admin_ctrl.router)
app.include_router(doctor_auth.router)
app.include_router(doctor_ctrl.router)
app.include_router(patient_auth.router)
app.include_router(patient_ctrl.router)