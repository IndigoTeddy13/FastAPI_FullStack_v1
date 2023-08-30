#Imports
import os, json #filepaths, JSONs
#from typing import Any, Dict, List, Union #different types
from email_validator import validate_email, EmailNotValidError #email validation
from fastapi import FastAPI, HTTPException #FastAPI stuff
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware #Allow CORS
#Personal imports
from .statRoute import *
from .authRoute import *
from .pydModels import *

#CORS PERMS:
#Allow at least these origins
origins:list = [
    "http://localhost", # implicit port 80
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080"
]

#Server Initialization
app = FastAPI() #initialize FastAPI
#Use CORSMiddleware to ensure CORS is permitted on this server
app.add_middleware(
    CORSMiddleware,  
    allow_origins=origins,# Allow all methods and headers, restrict origins
    allow_credentials=True, # True to allow cookies to be sent over
    allow_methods=["*"], 
    allow_headers=["*"]
)

#Static file management router
app.include_router(statRoute, prefix="/static")

#MongoDB management router
app.include_router(authRoute, prefix="/auth")

#API calls

#Request a Hello World JSON
@app.get("/")
async def helloWorld()-> dict:
    return {"Hello":"World"}
#Email validation
@app.post("/validate")
async def emailValidator(check:EmailCheck)-> str:
    try:
        emailinfo:object = validate_email(check.email, check_deliverability=check.verify)
        normalizedEmail:str = emailinfo.normalized
        return normalizedEmail
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=(str(e)))

# @app.get("/cookietest")
# async def cookieTest():
#     content = {"message": "Come to the dark side, we have cookies"}
#     response = JSONResponse(content=content)
#     response.set_cookie(
#         key="test",
#         value="test value goes here",
#         max_age=86400,
#         path="/",
#         httponly=True,
#         samesite="strict"
#     )
    
#     return response

# key: str,
# value: str = "",
# max_age: int | None = None,
# expires: datetime | str | int | None = None,
# path: str = "/",
# domain: str | None = None,
# secure: bool = False,
# httponly: bool = False,
# samesite: Literal['lax', 'strict', 'none'] | None = "lax"
