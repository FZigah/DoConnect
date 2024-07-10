from fastapi import APIRouter,status,Depends,HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from database.doctor_auth_profile_db import doctor_auth_collection, doctor_profile_collection
import schemas
from security import hashing, jwt_auth, oauth2_doctor
import pydantic
from bson.objectid import ObjectId
from datetime import datetime


pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

router = APIRouter(
    prefix="/api/v1",
    tags=["Doctor Auth"]
)

@router.post('/doctor_auth/signup')
async def create_doctor(request: schemas.DoctorSignUp):
    #hash user password
    user_hashed_password = hashing.Hash.get_pwd_hashed(request.password)
    try:
        # Creating doctor account with profile
        doctor = doctor_auth_collection.insert({
        "username": request.username,
        "email": request.email,
        "password": user_hashed_password,
        "createdAt": datetime.now()
    }) #This return user ID
        doctor_profile_collection.insert({
            "owner": doctor,
            "username": request.username,
            "status" : request.status,
            "experience": request.experience,
            "contacts": request.contacts,
            "createdAt": datetime.now()
        })

        return{
            "detail":"User created successfully"
        }
        
    except Exception as e:
        response = str(e)
        if "duplicate key error collection" in response:
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already registered")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
        

@router.post('/doctor_auth/login')
async def doctor_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    data = doctor_auth_collection.find_one({"email":form_data.username})
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")
    else:
        if hashing.Hash.verify_hashed_password(form_data.password, data["password"]):
           access_token = jwt_auth.create_access_token(data={"sub":str(data["_id"]),"sub_name":data["username"],"sub_role":'doctor'})
           return schemas.Token(access_token=access_token,token_type="bearer")   
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")