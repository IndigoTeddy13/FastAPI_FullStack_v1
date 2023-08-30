import os, json, asyncio #filepaths, JSONs, async requests
from fastapi import APIRouter, HTTPException, Request #FastAPI stuff
from .drivers.mongo import testMongo
from .drivers.redis import testRedis
# MongoDB management route:
authRoute = APIRouter()

@authRoute.get("/")
async def authHome()->dict:
    return {
        "mongo_healthCheck":await testMongo(),
        "redis_healthCheck":await testRedis()
    }

@authRoute.get("/refresh-token")
async def refreshToken(request:Request):
    #check if refresh token cookie is there
    if(request.cookies):
        return "refreshed jwt"
    else:
        raise HTTPException(status_code=401, detail="Login expired. Log in again.")
    

@authRoute.post("/register")
async def register():
    return "registered"

@authRoute.post("/login")
async def login():
    return "logged in"

@authRoute.get("/profile")
async def getProfile():
    return "profile"

@authRoute.put("/change-password")
async def changePassword():
    return "password changed"

@authRoute.delete("/logout")
async def logout():
    return "logged out"
