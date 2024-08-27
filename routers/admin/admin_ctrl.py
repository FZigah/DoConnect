from fastapi import APIRouter,status,Depends,HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
import schemas
from database.doctor_auth_profile_db import doctor_auth_collection, doctor_profile_collection
from database.patient_auth_profile_db import patient_auth_collection, patient_profile_collection
from security import oauth2_admin
import pydantic
from bson.objectid import ObjectId



pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

router = APIRouter(
    prefix="/api/v1",
    tags=["Admin Ctrl"]
)


#status

#Overview

#chat

@router.get('/admin/users')
async def get_all_users(current_user: schemas.User = Depends(oauth2_admin.get_current_user)):
    if current_user.user_role == "admin":
        try:
            doctors_profile = doctor_profile_collection.find({})
            patients_profile = patient_profile_collection.find({})
            return {
                    "doctors_profile": list(doctors_profile),
                    "patients_profile": list(patients_profile)
                }
        except Exception as e:
            response = str(e)
            raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= response)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")

@router.delete("/admin/users/doctor/")
async def delete_doctor(id: str, current_user: schemas.User = Depends(oauth2_admin.get_current_user)):

    if current_user.user_role == "admin":
             doctor_auth = doctor_auth_collection.find_one_and_delete({"_id": ObjectId(id)})
             doctor_profile = doctor_profile_collection.find_one_and_delete({"owner": ObjectId(id)})
             if doctor_profile and doctor_auth:
                return {"detail" : "Successfully deleted"}
             else:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")
    
@router.delete("/admin/users/patient/")
async def delete_patient(id: str, current_user: schemas.User = Depends(oauth2_admin.get_current_user)):
    if current_user.user_role == "admin":
             patient_auth = patient_auth_collection.find_one_and_delete({"_id": ObjectId(id)})
             patient_profile = patient_profile_collection.find_one_and_delete({"owner": ObjectId(id)})
             if patient_profile and patient_auth:
                return {"detail" : "Successfully deleted"}
             else:
                 raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Access denied")