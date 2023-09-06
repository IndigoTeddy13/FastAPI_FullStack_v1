import os, json, asyncio, uuid #filepaths, JSONs, async requests
from fastapi import APIRouter, HTTPException, Request, Depends #FastAPI stuff
from fastapi.responses import RedirectResponse #email validation
from passlib.context import CryptContext
#Mail handlers
from email_validator import validate_email, EmailNotValidError
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from fastapi_mail.email_utils import DefaultChecker
#Personal imports
from .drivers.mongo import *
from .pydModels import *

#Mongo Account Collection Setup

userColl = mongoClient[FastAPI_DB]["Users"]

#Configure FastAPI-Mail connection
conf = ConnectionConfig(
    MAIL_USERNAME = str(os.getenv("MAIL_USERNAME")),
    MAIL_PASSWORD = str(os.getenv("MAIL_PASSWORD")),
    MAIL_FROM = str(os.getenv("MAIL_FROM")),
    MAIL_PORT = int(str(os.getenv("MAIL_PORT"))),
    MAIL_SERVER = str(os.getenv("MAIL_SERVER")),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
)

async def default_checker():
    checker = DefaultChecker()
    await checker.fetch_temp_email_domains() # require to fetch temporary email domains
    return checker

#Password hashing functions
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hashPassword(password):
    return pwd_context.hash(password)

# Account management route:
authRoute = APIRouter()

@authRoute.get("/")
async def authHome():
    return await testMongo()

@authRoute.post("/activate/{email}")
async def activateEmail(request:Request, email:EmailStr, checker:DefaultChecker=Depends(default_checker)): # Need code for registration
    #Check if email string is valid
    normalizedEmail:EmailStr
    try:
        emailinfo:object = validate_email(
            email=email,
            check_deliverability=True
        )
        normalizedEmail = emailinfo.normalized
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=(str(e)))
    #Ensure email isn't disposable
    if await checker.is_disposable(normalizedEmail):
        HTTPException(status_code=400, detail="No disposable emails allowed.")
    
    #Send email with activation code
    request.session["activation"] = {
        "email":normalizedEmail,
        "code":int(uuid.uuid4())
    }
    message = MessageSchema(
        subject="Activation code for: " +normalizedEmail,
        recipients=[normalizedEmail],
        body="Activation Code: "+ str(request.session["activation"]["code"]),
        subtype=MessageType.html)
    fm = FastMail(conf)
    await fm.send_message(message)
    return "Email sent with activation code"

@authRoute.post("/refresh-token")# Most likely called on page load and after login on frontend
async def refreshToken(request:Request):
    #Check if a session is active
    if(request.session and request.session["user"]):
        #Store new access token for comparison (invalidates old tokens)
        request.session["token"] = "refreshed jwt"
        return request.session["token"] #return new access token
    else:
        raise HTTPException(status_code=401, detail="Login expired. Log in again.")
    

@authRoute.post("/register")
async def register(request:Request, user:RegUser):
    #Check if activation codes match
    if(not(request.session)):
        raise HTTPException(status_code=404, detail="Activate your email first!")
    if(not(request.session["activation"]=={
        "email":user.email,
        "code":user.activationCode
    })):
        raise HTTPException(status_code=400, detail="Get a new activation code and try again!")
    
    #Check user's email isn't registered in DB
    newUser:UserEntry = UserEntry(
        email=user.email,
        hash=hashPassword(user.password),
        displayName=user.displayName
    )
    # possibleUser = await queryToDict(userColl.find({"email":str(user.email)}))
    # if (not type(possibleUser)):
    #     raise HTTPException(status_code=409, detail="User already registered")
    # #Add to DB
    # await userColl.insert_one(newUser.model_dump())

    #redirect user to login
    return [newUser, "Registered. Now log into your account!"]

@authRoute.post("/login")
async def login(request:Request, user:LoginUser):
    # Check against main DB
    
    # Clear pre-existing session if re-logging in to ensure the older access token gets invalidated
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