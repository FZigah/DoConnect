from fastapi import APIRouter,status,Depends,HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from database.patient_auth_profile_db import patient_auth_collection, patient_profile_collection
import schemas
from security import hashing, jwt_auth, oauth2_patient
import pydantic
from bson.objectid import ObjectId
from datetime import datetime,date


pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

router = APIRouter(
    prefix="/api/v1",
    tags=["patient Auth"]
)

@router.post('/patient_auth/signup')
async def create_patient(request: schemas.PatientSignUp):
    #hash user password
    user_hashed_password = hashing.Hash.get_pwd_hashed(request.password)
    try:
        # Creating patient account with profile
        patient = patient_auth_collection.insert({
        "username": request.username,
        "email": request.email,
        "password": user_hashed_password,
        "createdAt": datetime.now()
    }) #This return user ID
        patient_profile_collection.insert({
            "owner": patient,
            "username": request.username,
            "gender": request.gender,
            "birthdate": request.birthdate,
            "profile_picture_url": request.profile_picture_url,
            "medicalHistory": request.medicalHistory,
            "medicalInfo": {
                "bloodtype": request.medicalInfo.bloodtype,
                "genotype": request.medicalInfo.genotype
            },
            "contacts": request.contacts,
            "createdAt": datetime.now()
        })

        return{
            "detail":"User created successfully"
        }
        
    except Exception as e:
        response = str(e)
        if "duplicate key error collection" in response:
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already is already registered")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
        

@router.post('/patient_auth/login')
async def patient_login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    data = patient_auth_collection.find_one({"email":form_data.username})
    if not data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")
    else:
        if hashing.Hash.verify_hashed_password(form_data.password, data["password"]):
           access_token = jwt_auth.create_access_token(data={"sub":str(data["_id"]),"sub_name":data["username"],"sub_role":'patient'})
           return schemas.Token(access_token=access_token,token_type="bearer")   
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials")

