from typing import Optional #Optional type for certain values
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ValidationError, field_validator #Models used in personal model definitions
from pydantic_core.core_schema import FieldValidationInfo

class Textfile(BaseModel):
    content:str

#Account classes
class RegUser(BaseModel):
    email:EmailStr
    password:str = Field(..., min_length=3, max_length=50) # 3 to 50 characters long
    passConf:str = Field(..., min_length=3, max_length=50)
    displayName:str = Field(..., min_length=1, max_length=30) # 1 to 30 characters long
    activationCode:int
    
    @field_validator("passConf")
    def passwords_match(cls, v:str, info:FieldValidationInfo) -> str:
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v

class UserEntry(BaseModel):
    email:EmailStr
    hash:str # store hash of password here
    displayName:str = Field(..., min_length=1, max_length=30)
    created:datetime = datetime.utcnow()
    admin:bool=False #default not an admin

class LoginUser(BaseModel):
    email:EmailStr
    password:str = Field(..., min_length=3, max_length=50)

class ChangeUserPass(BaseModel): # currently only allow changing password of logged-in user
    email:Optional[EmailStr] # Either log in or provide email and activation code
    newPass:str = Field(..., min_length=3, max_length=50)
    newPassConf:str = Field(..., min_length=3, max_length=50)
    activationCode:Optional[int]

    @field_validator("newPassConf")
    def passwords_match(cls, v:str, info:FieldValidationInfo) -> str:
        if "newPass" in info.data and v != info.data["newPass"]:
            raise ValueError("Passwords do not match")
        return v

class ChangeUserName(BaseModel):
    displayName:str = Field(..., min_length=1, max_length=30)
