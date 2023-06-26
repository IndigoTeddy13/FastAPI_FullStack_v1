from fastapi import FastAPI

app = FastAPI()

#API calls:
#Get root request (example)
@app.get("/")
async def root():
    return {"message": "Hello World"}

#Gotta check out how to set up port and IP manually later