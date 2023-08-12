import os, json #filepaths, JSONs
from motor import motor_asyncio #async connections to MongoDB
from fastapi import FastAPI, HTTPException #FastAPI stuff

# MongoDB management route:
mongoRoute = FastAPI()

mongoRoute.get("/")
async def mongoRoot()->dict:
    return {"Hello":"MongoDB"}