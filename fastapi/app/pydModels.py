from typing import Optional #Optional type for certain values
from pydantic import BaseModel, EmailStr #Models used in personal model definitions

class EmailCheck(BaseModel):
    email:EmailStr
    verify:bool=False

class Textfile(BaseModel):
    content:str

#Login classes
class User(BaseModel):
    username: str
    company: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
