import os, json, asyncio #filepaths, JSONs, async requests
from fastapi import APIRouter, HTTPException #FastAPI stuff
from .dbDriver import testMongo, testMaria
# MongoDB management route:
signinRoute = APIRouter()

@signinRoute.get("/")
async def signinHome()->dict:
    return {
        "mongo":await testMongo(),
        "maria":await testMaria()
    }