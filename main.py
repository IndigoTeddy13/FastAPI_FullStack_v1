#Imports
import os.path as paths #filepaths
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
#Server Initialization
app = FastAPI()#initialize FastAPI
sub = FastAPI()#for backend servicing
app.mount("/api", sub)#mount sub to handle backend stuff
templates = Jinja2Templates(directory="static")

#API calls:

#Homepage
@app.get('/', response_class=HTMLResponse)
async def index(request: Request):#default page
    return templates.TemplateResponse("index.html", {"request": request})

#Frontend page servicing
@app.get('/{name}', response_class=HTMLResponse)
async def index(request: Request, name: str):#default page
    #if the .html file exists
    if(paths.isfile("./static/"+name+".html")):
        #Homepage redirect
        if(name=="index"):
            return RedirectResponse(url="/")
        #Direct to requested HTML page
        else:
            return templates.TemplateResponse(name+".html", {"request": request})
    #Redirect to fix URL endpoint
    elif(paths.isfile("./static/"+name)):
        return RedirectResponse(url="/"+name.split(".html")[0])
    #Last resorts
    else:
        #If forgot to write "/" after "/api"
        if(name=="api"):
            return RedirectResponse(url="/api/")
        #otherwise, redirect to home page for safety (might reroute to an error page later on)
        else:
            return RedirectResponse(url="/")

#Backend API calls
#Request a Hello World JSON
@sub.get("/")
async def helloWorld():
    return {"Hello": "World"}

#Gotta check out how to set up port and IP manually later