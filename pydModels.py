from pydantic import BaseModel, EmailStr

class EmailCheck(BaseModel):
    email:EmailStr
    verify:bool=False