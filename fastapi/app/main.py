#Imports
import os, json #filepaths, JSONs
#from typing import Any, Dict, List, Union #different types
from fastapi import Depends, FastAPI, HTTPException #FastAPI stuff
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware #Allow CORS
#Personal imports
from .statRoute import *
from .authRoute import *
from .pydModels import *
from .drivers.mongo import *
from .drivers.redis import redisURL
#Redis Session Storage configuration
from starsessions import load_session, SessionMiddleware, SessionAutoloadMiddleware
from starsessions.stores.redis import RedisStore
session_store = RedisStore(url=redisURL, gc_ttl=3600)

#CORS PERMS:
#Allow at least these origins
origins:list = [
    "http://localhost", # implicit port 80
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080"
]

#Middlewares to add to the app:
middlewareList:list=[
    Middleware( # Use CORSMiddleware to ensure CORS is permitted on this server
        CORSMiddleware,  
        allow_origins=origins,# Allow all methods and headers, restrict origins
        allow_credentials=True, # True to allow cookies to be sent over
        allow_methods=["*"], 
        allow_headers=["*"]
    ),
    Middleware(
        SessionMiddleware,
        store=session_store,
        lifetime=1800, #Session lives up to 30 minutes from previous activity
        rolling=True,
        cookie_same_site= "strict",
        cookie_https_only=False,
        cookie_path="/"
    ),
    Middleware(SessionAutoloadMiddleware)
]

#Server Initialization
app = FastAPI(middleware=middlewareList) #initialize FastAPI

#Static file management router
app.include_router(statRoute, prefix="/static")

#MongoDB management router
app.include_router(authRoute, prefix="/auth")

#API calls

#Request a Hello World JSON
@app.get("/")
async def helloWorld()-> dict:
    return {"Hello":"World"}