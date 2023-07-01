from typing import Optional #Optional type for certain values
from pydantic import BaseModel, EmailStr #Models used in personal model definitions

class EmailCheck(BaseModel):
    email:EmailStr
    verify:bool=False

class Textfile(BaseModel):
    content:str