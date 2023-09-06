from typing import Optional #Optional type for certain values
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, root_validator #Models used in personal model definitions
from uuid import UUID, uuid4

class Textfile(BaseModel):
    content:str

#Account classes
class RegUser(BaseModel):
    email:EmailStr
    password:str = Field(..., min_length=3, max_length=50) # 3 to 50 characters long
    passConf:str = Field(..., min_length=3, max_length=50)
    displayName:str = Field(..., min_length=1, max_length=30) # 1 to 30 characters long
    activationCode:str

    @root_validator()
    def verify_password_match(cls,values):
        password = values.get("password")
        passConf = values.get("passConf")

        if (password != passConf):
            raise ValueError("The two passwords did not match.")
        return values

class UserEntry(BaseModel):
    email:EmailStr
    hash:str # store hash of password here
    displayName:str = Field(..., min_length=1, max_length=30)
    created:datetime = datetime.utcnow()
    activated:bool=False #default unactivated
    admin:bool=False #default not an admin

class LoginUser(BaseModel):
    email:EmailStr
    password:str = Field(..., min_length=3, max_length=50)

class ChangeUserPass(BaseModel): # currently only allow changing password of logged-in user
    newPass:str = Field(..., min_length=3, max_length=50)
    newPassConf:str = Field(..., min_length=3, max_length=50)

    @root_validator()
    def verify_password_match(cls,values):
        newPass = values.get("newPass")
        newPassConf = values.get("newPassConf")

        if (newPass != newPassConf):
            raise ValueError("The two passwords did not match.")
        return values
