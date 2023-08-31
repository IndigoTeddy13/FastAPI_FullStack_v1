from typing import Optional #Optional type for certain values
from pydantic import BaseModel, EmailStr, Field #Models used in personal model definitions
from uuid import UUID, uuid4

class EmailCheck(BaseModel):
    email:EmailStr
    verify:bool=False

class Textfile(BaseModel):
    content:str

#Login classes
class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email:EmailStr
    password:str
    displayName:str
    activated:bool=False

class Login(BaseModel):
    email:str
    password:str
