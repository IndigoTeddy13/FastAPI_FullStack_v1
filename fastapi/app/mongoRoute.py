import os, json, asyncio #filepaths, JSONs, async requests
from motor.motor_asyncio import AsyncIOMotorClient #async connections to MongoDB
from fastapi import FastAPI, APIRouter, HTTPException #FastAPI stuff

# MongoDB management route:
mongoRoute = APIRouter()

@mongoRoute.get("/")
async def mongoRoot()->dict:
    return {"Hello":"MongoDB"}