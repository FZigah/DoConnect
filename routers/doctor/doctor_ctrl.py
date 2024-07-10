from fastapi import APIRouter,status,Depends,HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
import schemas
from database.doctor_auth_profile_db import doctor_profile_collection
from database.doctor_auth_profile_db import  doctor_profile_collection, doctor_auth_collection
from database.appointments import appointments_collection
from security import oauth2_doctor
import pydantic
from bson.objectid import ObjectId
from datetime import datetime,date

pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

router = APIRouter(
    prefix="/api/v1",
    tags=["Doctor Ctrl"]
)

@router.get('/doctor')
async def get_doctor_profile(current_user: schemas.User = Depends(oauth2_doctor.get_current_user)):
    if current_user.user_role == "doctor":
        try:
         return doctor_profile_collection.find_one({"owner": ObjectId(current_user.user_id)})
        except Exception as e:
            response = str(e)
            raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= response)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")
    
@router.patch('/doctor')
async def update_doctor_profile(current_user: schemas.User = Depends(oauth2_doctor.get_current_user)):
   pass

@router.delete('/doctor')
async def delete_doctor_account(current_user: schemas.User = Depends(oauth2_doctor.get_current_user)):
    if current_user.user_role == "doctor":
             doctor_auth = doctor_auth_collection.find_one_and_delete({"_id": ObjectId(current_user.user_id)})
             doctor_profile = doctor_profile_collection.find_one_and_delete({"owner": ObjectId(current_user.user_id)})
             if doctor_profile and doctor_auth:
                return {"detail" : "Successfully deleted"}
             else:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")
    
@router.get('/doctor/appointment')
async def get_doctor_appointment(current_user: schemas.User = Depends(oauth2_doctor.get_current_user)):
    if current_user.user_role == "doctor":
        try:
            doctor_appointment = appointments_collection.find({"doctor_id":ObjectId(current_user.user_id)})
            return {
                    "appointments": list(doctor_appointment)
                }
        except Exception as e:
            response = str(e)
            raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= response)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")
    
@router.patch("doctor/appointment/{id}")
async def update_appointment(request: schemas.AppointmentStatus, id:str, current_user: schemas.User = Depends(oauth2_doctor.get_current_user)):
    if current_user.user_role == "doctor":
        try:
            appointments_collection.find_one_and_update({"_id": ObjectId(id)},{'$set':{ "appointment_status": request.appointment_status}})
            return{"detail": "Appointment has been updated successfully"}
        except Exception as e:
            response = str(e)
            raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= response)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")