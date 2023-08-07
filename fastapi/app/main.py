#Imports
import os, json #filepaths, JSONs
from typing import Any, Dict, List, Union #different types
from email_validator import validate_email, EmailNotValidError #email validation
from fastapi import FastAPI, HTTPException #FastAPI stuff
from starlette.middleware.cors import CORSMiddleware #Allow CORS
from fastapi.responses import FileResponse # send text files to users
#Personal imports
from .statRoute import *
from .pydModels import *

#CORS PERMS:
#Allow at least these origins
origins:list = [
    "http://localhost", # implicit port 80
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080"
]
#Allow all kinds of methods
methods:list = [
    "GET", "POST", "PULL", "DELETE",
    "PATCH", "HEAD", "OPTIONS",
    "CONNECT", "TRACE"
] 
#Server Initialization
app = FastAPI() #initialize FastAPI
#Use CORSMiddleware to ensure CORS is permitted on this server
app.add_middleware(
    CORSMiddleware,  
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=methods,
    allow_headers=["*"]#Not sure what headers to block, so allow all for now
)

#Static file management router
app.mount("/static", statRoute)

#MongoDB management router
mongoRoute = FastAPI()
app.mount("/db", mongoRoute)

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
        return(str(e))



