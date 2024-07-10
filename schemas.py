from pydantic import BaseModel
from typing import Union, Annotated
from datetime import datetime

class TokenData(BaseModel):
    user_id: Union[str, None] = None
    user_name: str
    user_role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class AdminSignUp(BaseModel):
    username: str
    password: str
    email: str

class DoctorContacts(BaseModel):
    contact1: str
    contact2: str

class DoctorSignUp(BaseModel):
    username: str
    email: str
    password: str
    status: Union[str, None] = None
    experience: str
    contacts: Union[list,DoctorContacts]

class PatientContacts(BaseModel):
    contact1: str
    contact2: str

class PatientmedicalInfo(BaseModel):
    bloodtype: str
    genotype: str

class PatientmedicalHistory(BaseModel):
    typeOfSickness: str
    period: int

class PatientSignUp(BaseModel):
    username: str
    email: str
    password: str
    birthdate: datetime
    contacts: Union[list,PatientContacts]
    medicalInfo: PatientmedicalInfo
    medicalHistory: Union[list, PatientmedicalHistory]
    gender: str
    profile_picture_url: Annotated[str,None] = "http://localhost:8000/patientsprofilepicture/default.png"
    

class User(BaseModel):
    user_id: Union[str, None] = None
    user_name: str
    user_role: str

class Appointment(BaseModel):
    patient_description: str
    doctor_id: Union[str, None] = None
    doctor_name: str
    patient_profile_picture_url: Annotated[str,None] = "http://localhost:8000/patientsprofilepicture/default.png"
    appointment_status: Annotated[str,None] = "pending"

class AppointmentStatus(BaseModel):
    appointment_status: str

class DoctorRating(BaseModel):
    rating:str