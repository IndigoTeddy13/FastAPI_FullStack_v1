import os, json #filepaths, JSONs
from motor import motor_asyncio #async connections to MongoDB
from fastapi import FastAPI, APIRouter, HTTPException #FastAPI stuff

# MongoDB management route:
mongoRoute = APIRouter()

@mongoRoute.get("/")
async def mongoRoot()->dict:
    return {"Hello":"MongoDB"}