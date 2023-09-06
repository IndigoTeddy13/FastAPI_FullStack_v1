import os, json, asyncio #filepaths, JSONs, async requests
from fastapi import APIRouter, HTTPException, Request #FastAPI stuff
from email_validator import validate_email, EmailNotValidError
from fastapi.responses import RedirectResponse #email validation
from passlib.context import CryptContext
#Personal imports
from .drivers.mongo import *
from .pydModels import *

#Password hashing functions
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hashPassword(password):
    return pwd_context.hash(password)

# Account management route:
authRoute = APIRouter()

@authRoute.get("/")
async def authHome()->dict:
    return await testMongo()

@authRoute.put("/refresh-token")# Most likely called on page load and after login on frontend
async def refreshToken(request:Request):
    #Check if a session is active
    if(request.session):
        #Store new access token for comparison (invalidates old tokens)
        request.session["active-token"] = "refreshed jwt"
        return request.session["active-token"] #return new access token
    else:
        raise HTTPException(status_code=401, detail="Login expired. Log in again.")
    

@authRoute.post("/register")
async def register(user:RegUser):
    #check email string is valid
    normalizedEmail:EmailStr
    try:
        emailinfo:object = validate_email(
            email=user.email,
            check_deliverability=True
        )
        normalizedEmail = EmailStr(emailinfo.normalized)
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=(str(e)))
    #add to main DB
    newUser:UserEntry = UserEntry(
        email=normalizedEmail,
        hash=hashPassword(user.password),
        displayName=user.displayName
    )
    #redirect user to login
    return newUser

@authRoute.post("/login")
async def login(request:Request, user:LoginUser):
    # Check against main DB
    
    # Clear pre-existing session if re-logging in
    # Ensures the older access token gets invalidated
    if(request.session):
        request.session.clear()

    #Start a new session
    request.session["user"]={
        "user":user.email,
        "password":user.password
    }
    return "logged in"

@authRoute.get("/profile")
async def getProfile(request:Request):
    #grab requested user data
    #return after proper formatting to hid sensitive info (UID, password hash, etc)
    return request.session

@authRoute.put("/change-password")
async def changePassword(request:Request, user:ChangeUserPass):
    #Confirm user is logged in
    if not(request.session):
        raise HTTPException(status_code=400, detail="Log in with your account to try changing your password")
    #check against main DB for requested user
    #change password
    request.session["user"]["password"] = user.newPass
    return "password changed"

@authRoute.delete("/logout")
async def logout(request:Request):
    #clear session, which invalidates access tokens automatically
    request.session.clear() 
    return "logged out"

# #Email validation
# @authRoute.post("/validate")
# async def emailValidator(check:EmailCheck)-> str:
#     try:
#         emailinfo:object = validate_email(check.email, check_deliverability=check.verify)
#         normalizedEmail:str = emailinfo.normalized
#         return normalizedEmail
#     except EmailNotValidError as e:
#         raise HTTPException(status_code=400, detail=(str(e)))
# #Server session tests:
# @app.get("/set")
# async def set_session(request:Request):
#     request.session["key"] = "value"
#     return "Key stored!"

# @app.get("/get")
# async def get_session(request:Request):
#     return request.session

# @app.get("/clear")
# async def clear_session(request:Request):
#     request.session.clear()
#     return "Cleared session!"