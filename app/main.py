#Imports
import os, json #filepaths, JSONs
from typing import Any, Dict, List, Union #different types
from email_validator import validate_email, EmailNotValidError #email validation
from fastapi import FastAPI, HTTPException #FastAPI stuff
from starlette.middleware.cors import CORSMiddleware #Allow CORS
from fastapi.responses import FileResponse # send text files to users
#Personal imports
from .pydModels import *

#CORS PERMS:
#Allow at least these origins
origins:list = [
    "http://localhost:80",
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
statRoute = FastAPI()
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

#Static CRUD check

#Request a specific greeting
@statRoute.get("/{filename}")#greet person by name and return their request body
async def helloGetter(filename:str)-> FileResponse:
    targetFile:str = os.path.join(os.getcwd(), "app", "static") +"/"+ filename+".txt" #request params
    if(os.path.exists(targetFile)):
        output:str
        with open(targetFile, 'r', encoding='utf-8') as f:
            output = f.read()
        return FileResponse(targetFile) #return file to user
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#Post new file if name is unused
@statRoute.post("/{filename}")
async def helloPoster(filename:str, body:Textfile)-> str:
    targetFile:str = filename+".txt" #request params
    targetPath:str = os.path.join(os.getcwd(), "app", "static")
    if (not(os.path.exists(targetPath))):
        os.makedirs(targetPath)#make directory if it doesn't exist
    newPath:str = targetPath+"/"+targetFile
    if(not(os.path.exists(newPath))):
        with open(newPath, 'w', encoding='utf-8') as f:
            f.write(body.content)
        return ("Posted "+ filename +" successfully!")
    else:
        raise HTTPException(status_code=404, detail="Item already exists")

#Overwrite specified file
@statRoute.put("/{filename}")
async def helloPutter(filename:str, body:Textfile)-> str:
    targetFile:str = os.path.join(os.getcwd(), "app", "static") +"/"+ filename+".txt" #request params
    if(os.path.exists(targetFile)):
        with open(targetFile, 'w', encoding='utf-8') as f:
            f.write(body.content)
        return ("Replaced "+ filename + " successfully!")
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#Add to specified file
@statRoute.patch("/{filename}")
async def helloPatcher(filename:str, body:Textfile)-> str:
    targetFile:str = os.path.join(os.getcwd(), "app", "static") +"/"+ filename+".txt" #request params
    if(os.path.exists(targetFile)):
        with open(targetFile, 'a', encoding='utf-8') as f:
            f.write("\n" + body.content)
        return ("Added to "+ filename + " successfully!")
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#Delete specified file
@statRoute.delete("/{filename}")
async def helloRemover(filename:str)-> str:
    targetFile:str = os.path.join(os.getcwd(), "app", "static") +"/"+ filename+".txt" #request params
    if(os.path.exists(targetFile)):
        os.remove(targetFile) #removed the file if it still
        return str(filename +" was successfully deleted!")
    else:
        raise HTTPException(status_code=404, detail="Item not found")

