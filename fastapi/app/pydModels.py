from typing import Optional #Optional type for certain values
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field #Models used in personal model definitions
from uuid import UUID, uuid4

class Textfile(BaseModel):
    content:str

#Account classes
class RegUser(BaseModel):
    email:EmailStr
    password:str
    passConf:str
    displayName:str
    activationCode:str

class UserEntry(BaseModel):
    email:EmailStr
    hash:str
    displayName:str
    created:datetime = datetime.utcnow()
    admin:bool=False

class LoginUser(BaseModel):
    email:EmailStr
    password:str

class ChangeUserPass(BaseModel):
    newPass:str
    newPassConf:str
