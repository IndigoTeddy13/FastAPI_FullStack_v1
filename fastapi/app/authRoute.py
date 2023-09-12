import os, uuid #filepaths, JSONs, async requests
from fastapi import APIRouter, HTTPException, Request, Depends #FastAPI stuff
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

#Check anti-CSRF token on authenticated routes
async def checkUser(request:Request, needToken:bool=False):
    if not(request.session and request.session.get("user")):
        raise HTTPException(status_code=403, detail="User isn't logged in properly. Log in and try again.")
    if (needToken) and not(request.session.get("token")==request.headers.get("Anti-CSRF")):
        raise HTTPException(status_code=403, detail="User didn't provide the correct Anti-CSRF token in header. Fetch a new token and try again.")
    return True
    

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
        emailinfo = validate_email(
            email=email,
            check_deliverability=True
        )
        normalizedEmail = emailinfo.normalized
    except EmailNotValidError as e:
        raise HTTPException(status_code=400, detail=(str(e)))
    #Ensure email isn't disposable
    if await checker.is_disposable(normalizedEmail):
        HTTPException(status_code=400, detail="No disposable emails are allowed.")
    
    #Send email with activation code
    request.session["activation"] = {
        "email":normalizedEmail,
        "code":str(uuid.uuid4())
    }
    message = MessageSchema(
        subject="Activation code for: " +normalizedEmail,
        recipients=[normalizedEmail],
        body="Activation Code: "+ str(request.session["activation"]["code"]),
        subtype=MessageType.html)
    fm = FastMail(conf)
    await fm.send_message(message)
    return "An email was sent with your activation code!"

@authRoute.post("/refresh-token")# Most likely called on page load and after login on frontend
async def refreshToken(request:Request):
    #Check if a session is active
    await checkUser(request=request)
    #Store new access token for comparison (invalidates old tokens)
    request.session["token"] = str(uuid.uuid4())
    return request.session["token"] #return new access token

@authRoute.post("/login")
async def login(request:Request, user:LoginUser):
    # Check against main DB
    possibleEntry = await userColl.find_one({"email":str(user.email)}, {'_id': 0})
    if not(possibleEntry):
        raise HTTPException(status_code=404, detail="Account doesn't exist. Activate your email and register first.")
    #Compare passwords
    possibleUser:UserEntry = UserEntry.model_validate(possibleEntry)
    if not(verifyPassword(plain_password=user.password, hashed_password=possibleUser.hash)):
        raise HTTPException(status_code=400, detail="Password is wrong. Try again or activate your email to change your password.")
    
    # Clear pre-existing session if re-logging in to ensure the older access token gets invalidated
    if(request.session):
        request.session.clear()

    #Start a new session
    request.session["user"] = possibleUser.email
    return await refreshToken(request=request)

@authRoute.post("/register")
async def register(request:Request, user:RegUser):
    #Check if activation codes match
    if(not(request.session)):
        raise HTTPException(status_code=404, detail="Activate your email first!")
    if(not(request.session.get("activation")=={
        "email":user.email,
        "code":user.activationCode
    })):
        raise HTTPException(status_code=403, detail="Get a new activation code and try again!")
    
    #Check user's email isn't registered in DB
    newUser:UserEntry = UserEntry(
        email=user.email,
        hash=hashPassword(user.password),
        displayName=user.displayName
    )
    possibleUser = await userColl.find_one({"email":str(user.email)})
    if (possibleUser):
        raise HTTPException(status_code=409, detail="Another user already registered with your email.")
    #Add to DB
    await userColl.insert_one(newUser.model_dump())

    # Clear pre-existing session to ensure activation code gets invalidated
    if(request.session):
        request.session.clear()

    #redirect user to login
    return await login(
        request=request,
        user=LoginUser(
            email=user.email,
            password=user.password
        )
    )

@authRoute.get("/profile")
async def getProfile(request:Request):
    await checkUser(request=request, needToken=True)
    
    #Retrieve full user info from main DB and format it accordingly
    possibleEntry = await userColl.find_one({"email":str(request.session["user"])}, {'_id': 0})
    if not(possibleEntry):
        raise HTTPException(status_code=404, detail="Account doesn't exist. Activate your email and register first.")
    possibleUser:UserEntry = UserEntry.model_validate(possibleEntry)
    return {
        "email":possibleUser.email,
        "displayName":possibleUser.displayName,
        "created":possibleUser.created,
        "admin":possibleUser.admin
    }

@authRoute.put("/change-password")
async def changePassword(request:Request, user:ChangeUserPass):
    #Confirm user's email is activated
    try: #Is the user logged in?
        await checkUser(request=request, needToken=True)
    except:
        #Is the user using an activated email because they forgot their password?
        try: 
            if(not(request.session.get("activation")=={
                "email":user.email,
                "code":user.activationCode
            })):
                raise HTTPException(status_code=403, detail="Get a new activation code or log in and try again!")
        except Exception as e: #Catch the exception and raise it
            raise (e)
    #check against main DB for requested user
    possibleEntry = await userColl.find_one({"email":str(user.email)}, {'_id': 0})
    if not(possibleEntry):
        raise HTTPException(status_code=404, detail="Account doesn't exist. Activate your email and register first.")
    #change password if user exists
    possibleUser:UserEntry = UserEntry.model_validate(possibleEntry)
    await userColl.update_one(
        {'email': possibleUser.email},
        {'$set': {'hash': hashPassword(user.newPass)}}
    )
    request.session.clear() # Force user to log in again
    return "Password changed. Now log in again!"

@authRoute.put("/change-name")
async def changeName(request:Request, user:ChangeUserName):
    #Confirm user is logged in
    await checkUser(request=request, needToken=True)
    #check against main DB for requested user
    possibleEntry = await userColl.find_one({"email":str(request.session["user"])}, {'_id': 0})
    if not(possibleEntry):
        raise HTTPException(status_code=404, detail="Account doesn't exist. Activate your email and register first.")
    #change password if user exists
    possibleUser:UserEntry = UserEntry.model_validate(possibleEntry)
    await userColl.update_one(
        {'email': possibleUser.email},
        {'$set': {'displayName': user.displayName}}
    )
    return "Name changed to {newName} successfully!".format(newName=user.displayName)

@authRoute.delete("/logout")
async def logout(request:Request):
    #clear session, which invalidates access tokens automatically
    request.session.clear() 
    return "Logged out successfully!"

@authRoute.delete("/delete-account")
async def deleteAccount(request:Request):
    #Confirm user is logged in
    await checkUser(request=request, needToken=True)
    #Remove user if user exists
    await userColl.find_one_and_delete({"email":str(request.session["user"])})
    request.session.clear()
    return "Your account is now deleted! Register to start all over."
