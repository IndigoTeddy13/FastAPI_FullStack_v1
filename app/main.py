#Imports
import os, json #filepaths, JSONs
#import uvicorn #runtime environment
from typing import Any, Dict, List, Union #different types
from email_validator import validate_email, EmailNotValidError #email validation
from fastapi import FastAPI, Request #FastAPI stuff
from starlette.middleware.cors import CORSMiddleware #Allow CORS
from fastapi.templating import Jinja2Templates #Routing/templating HTML files
from fastapi.responses import HTMLResponse, RedirectResponse #Responses
#Personal imports
from .pydModels import *


#Server Initialization
app = FastAPI() #initialize FastAPI
sub = FastAPI() #for backend servicing
app.mount("/api", sub) #mount sub to handle backend stuff
templates = Jinja2Templates(directory="app/static")

#CORS initialization
origins:list = [ #Set the origins
    "http://localhost:80",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080"
]
#Use CORSMiddleware to ensure CORS is permitted on this server
app.add_middleware(
    CORSMiddleware,  
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"], #set methods
    allow_headers=["*"]
)


#API calls
#Frontend calls

#Main page
@app.get('/', response_class=HTMLResponse)
async def index(request: Request): #default page
    return templates.TemplateResponse("index.html", {"request": request})
#Index reroute
@app.get('/index', response_class=HTMLResponse)
@app.get('/index.html', response_class=HTMLResponse)
async def indexReroute(request: Request): #default page
    return RedirectResponse(url="/")
#Reroute if typing "/api"
@app.get('/api', response_class=HTMLResponse)
async def apiReroute(request: Request): #default page
    return RedirectResponse(url="/api/")
#aaa page
@app.get('/aaa', response_class=HTMLResponse)
async def aaa(request: Request): #default page
    return templates.TemplateResponse("aaa.html", {"request": request})
#aaa reroute
@app.get('/aaa.html', response_class=HTMLResponse)
async def aaaReroute(request: Request):
    return RedirectResponse(url="/aaa")


#Backend API calls
#Handled by the "sub" app

#Request a Hello World JSON
@sub.get("/")
async def helloWorld():
    return {"Hello":"World"}
#Email validation
@sub.post("/validate")
async def emailValidator(check:EmailCheck):
    try:
        emailinfo:object = validate_email(check.email, check_deliverability=check.verify)
        normalizedEmail:str = emailinfo.normalized
        return normalizedEmail
    except EmailNotValidError as e:
        return(str(e))


#CRUD check

#Request a specific greeting
@sub.get("/{filename}")#greet person by name and return their request body
async def helloGetter(filename:str):
    getterTarget:str =  "./static/"+filename+".json" #request params
    if(os.path.exists(getterTarget)):
        #f = open(getterTarget)
        #output = json.load(f)
        #f.close()
        return {"Hello": filename}#str(output)
    else:
        return 0

#Post new file if name is unused
@sub.post("/{filename}")
async def helloPoster(filename:str, body:Union[List,Dict,Any]=None):
    posterTarget:str =  "./static/"+filename+".json" #request params
    if(not(os.path.exists(posterTarget))):
        #f = open(posterTarget, "x")#"x" creates a new file if it didn't exist before
        #output = json.dump(f)
        #f.close()
        return "posted"
    else:
        return 0

#Overwrite specified file
@sub.put("/{filename}")
async def helloPutter(filename:str, body:Union[List,Dict,Any]=None):
    putterTarget:str =  "./static/"+filename+".json" #request params
    if(os.path.exists(putterTarget)):
        #f = open(putterTarget) #open an existing file to change it
        #output = json.dump(f)
        #f.close()
        return "putted"
    else:
        return 0

#Delete specified file
@sub.delete("/{filename}")
async def helloRemover(filename:str):
    removerTarget:str =  "./static/"+filename+".json" #request params
    if(os.path.exists(removerTarget)):
        os.remove(removerTarget) #removed the file if it still
        return "deleted"
    else:
        return 0


#Programatically run uvicorn:
#if (__name__ == "__main__"):
#    uvicorn.run("main:app", host="localhost", port=int(os.environ.get('PORT', 8000)), log_level="info", reload=True)
#Gotta check out how to set up port and IP manually later