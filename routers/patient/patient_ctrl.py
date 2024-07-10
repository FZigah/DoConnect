from fastapi import APIRouter,status,Depends,HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
import schemas
from database.doctor_auth_profile_db import doctor_profile_collection
from database.patient_auth_profile_db import  patient_profile_collection, patient_auth_collection
from database.appointments import appointments_collection
from security import oauth2_patient, oauth2_doctor
import pydantic
from bson.objectid import ObjectId
from datetime import datetime,date


pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

router = APIRouter(
    prefix="/api/v1",
    tags=["Patient Ctrl"]
)

#chat

@router.get('/patient')
async def get_patient_profile(current_user: schemas.User = Depends(oauth2_patient.get_current_user)):
    if current_user.user_role == "patient":
        try:
         return patient_profile_collection.find_one({"owner": ObjectId(current_user.user_id)})
        except Exception as e:
            response = str(e)
            raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= response)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")
    

@router.patch('/patient')
async def update_patient_profile(current_user: schemas.User = Depends(oauth2_patient.get_current_user)):
    pass


@router.delete("/patient/{id}")
async def delete_patient_account(current_user: schemas.User = Depends(oauth2_patient.get_current_user)):
    if current_user.user_role == "patient":
             patient_auth = patient_auth_collection.find_one_and_delete({"_id": ObjectId(current_user.user_id)})
             patient_profile = patient_profile_collection.find_one_and_delete({"owner": ObjectId(current_user.user_id)})
             if patient_profile and patient_auth:
                return {"detail" : "Successfully deleted"}
             else:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")


@router.get('/patient/get-doctors')
async def get_all_doctors(current_user: schemas.User = Depends(oauth2_patient.get_current_user)):
    if current_user.user_role == "patient":
        try:
            doctors_profile = doctor_profile_collection.find({})
            return {
                    "doctors_profile": list(doctors_profile)
                }
        except Exception as e:
            response = str(e)
            raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= response)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")


@router.patch("/patient/rate-doctor/{id}")
async def rate_doctor(request:schemas.DoctorRating, id: str, current_user: schemas.User = Depends(oauth2_doctor.get_current_user)):
    if current_user.user_role == "patient":
        try:
            rating = doctor_profile_collection.find_one_and_update({"owner": ObjectId(id)},{'$push':{ "ratings": request.rating}})
            return{
                "detail" : "Successfully rated"
            }
        except Exception as e:
            response =str(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= response)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")


@router.get('/patient/appointments')
async def get_appointments(current_user: schemas.User = Depends(oauth2_patient.get_current_user)):
    if current_user.user_role == "patient":
        try:
            patient_appointment = appointments_collection.find({"patient_id":ObjectId(current_user.user_id)})
            return {
                    "appointments": list(patient_appointment)
                }
        except Exception as e:
            response = str(e)
            raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= response)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")

@router.post('/patient/appointments/create')
async def create_appointments(request:schemas.Appointment,current_user: schemas.User = Depends(oauth2_patient.get_current_user)):
    if current_user.user_role == "patient":
        try:
            patient_appointment = appointments_collection.insert({
                "patient_name": current_user.user_name,
                "patient_description": request.patient_description,
                "patient_id": ObjectId(current_user.user_id),
                "doctor_id": ObjectId(request.doctor_id),
                "doctor_name": request.doctor_name,
                "patient_profile_picture_url": request.patient_profile_picture_url,
                "appointment_status": request.appointment_status,
                "createdAt": datetime.now()
            })
            return {
                     "detail":"Appointment created successfully"
                }
        except Exception as e:
            response = str(e)
            raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= response)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")

@router.delete("/patient/appointments/{id}")
async def delete_appointment(id:str,current_user: schemas.User = Depends(oauth2_patient.get_current_user)):
    if current_user.user_role == "patient":
        try:
            patient_appointment = appointments_collection.find_one_and_delete({"_id": ObjectId(id)})
            return {
                     "detail":"Appointment deleted successfully"
                }
        except Exception as e:
            response = str(e)
            raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= response)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")