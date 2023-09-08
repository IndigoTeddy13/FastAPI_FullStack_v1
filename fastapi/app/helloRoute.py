#Imports
import os #filepaths
from fastapi import APIRouter, HTTPException, Request #FastAPI stuff
from fastapi.responses import Response # send markdown files to users
from pathvalidate import is_valid_filename # to validate an inputted filename
#Personal imports
from .pydModels import *
from .authRoute import checkUser
from .drivers.mongo import *

#Mongo Markdown Greetings Collection Setup
hellosColl = mongoClient[FastAPI_DB]["Greetings"]

#Static markdown file route:
hellosRoute = APIRouter()
staticDir:str = os.path.join(os.getcwd(), "app", "static")

#Function to check if a filename is valid
def validateFilename(fName:str):
    if(is_valid_filename(filename=str(fName+".md"))):
        return None
    else:
        raise HTTPException(status_code=400, detail="Not a valid name")

#Static CRUD check
@hellosRoute.get("/")
async def allHellos():
    if (not(os.path.exists(staticDir))):
        os.makedirs(staticDir)#make directory if it doesn't exist

    # Now check for the contents of staticDir
    helloList:list = os.listdir(staticDir)
    if(len(helloList)==0):
        raise HTTPException(status_code=404, detail="No greetings available at the moment")
    else:
        return [s.strip(".md") for s in helloList] # strip out the .md suffixes

#Request a specific greeting
@hellosRoute.get("/{filename}")#greet person by name and return their request body
async def helloGetter(filename:str):
    validateFilename(filename) #validate filename before proceeding
    targetFile:str = staticDir +"/"+ filename+".md" #request params
    #return targetFile
    if (not(os.path.exists(staticDir))):
        os.makedirs(staticDir)#make directory if it doesn't exist
    if(os.path.exists(targetFile)):
        with open(targetFile, 'r', encoding='utf-8') as f:
            fileContents:str = f.read()
        headerContent:dict = {
            'Content-Disposition': 'inline; filename="{fn}.md"'.format(fn=filename)
        }
        return Response(content=fileContents, headers=headerContent, media_type="text/markdown") #return file to user
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#Post new file if name is unused
@hellosRoute.post("/{filename}")
async def helloPoster(filename:str, body:Markdown, request:Request):
    #Ensure the user is logged in first
    await checkUser(request=request, needToken=True)
    #Write the file
    validateFilename(filename) #validate filename before proceeding
    targetFile:str = filename+".md" #request params
    #return targetFile
    if (not(os.path.exists(staticDir))):
        os.makedirs(staticDir)#make directory if it doesn't exist
    
    newPath:str = staticDir+"/"+targetFile
    if(not(os.path.exists(newPath))):
        with open(newPath, 'w', encoding='utf-8') as f:
            f.write(body.content)
        return ("Posted "+ filename +" successfully!")
    else:
        raise HTTPException(status_code=404, detail="Item already exists")

#Overwrite specified file
@hellosRoute.put("/{filename}")
async def helloPutter(filename:str, body:Markdown, request:Request):
    #Ensure the user is logged in first
    await checkUser(request=request, needToken=True)
    #Replace the file
    validateFilename(filename) #validate filename before proceeding
    targetFile:str = staticDir +"/"+ filename+".md" #request params
    #return targetFile
    if(os.path.exists(targetFile)):
        with open(targetFile, 'w', encoding='utf-8') as f:
            f.write(body.content)
        return ("Replaced "+ filename + " successfully!")
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#Add to specified file
@hellosRoute.patch("/{filename}")
async def helloPatcher(filename:str, body:Markdown, request:Request):
    #Ensure the user is logged in first
    await checkUser(request=request, needToken=True)
    #Append to the file
    validateFilename(filename) #validate filename before proceeding
    targetFile:str = staticDir +"/"+ filename+".md" #request params
    #return targetFile
    if(os.path.exists(targetFile)):
        with open(targetFile, 'a', encoding='utf-8') as f:
            f.write("\n" + body.content)
        return ("Added to "+ filename + " successfully!")
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#Delete specified file
@hellosRoute.delete("/{filename}")
async def helloRemover(filename:str, request:Request):
    #Ensure the user is logged in first
    await checkUser(request=request, needToken=True)
    #Remove the file
    validateFilename(filename) #validate filename before proceeding
    targetFile:str = staticDir +"/"+ filename+".md" #request params
    #return targetFile
    if(os.path.exists(targetFile)):
        os.remove(targetFile) #removed the file if it still
        return str(filename +" was successfully deleted!")
    else:
        raise HTTPException(status_code=404, detail="Item not found")