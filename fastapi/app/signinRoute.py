import os, json, asyncio #filepaths, JSONs, async requests
from fastapi import APIRouter, HTTPException #FastAPI stuff

# MongoDB management route:
signinRoute = APIRouter()

@signinRoute.get("/")
async def signinHome()->dict:
    return {"Hello":"Logger"}