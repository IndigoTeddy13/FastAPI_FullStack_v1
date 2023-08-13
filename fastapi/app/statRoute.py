#Imports
import os #filepaths
from fastapi import FastAPI, APIRouter, HTTPException #FastAPI stuff
from fastapi.responses import FileResponse # send text files to users
from pathvalidate import is_valid_filename # to validate an inputted filename
#Personal imports
from .pydModels import *

#Static text file route:
statRoute = APIRouter()
staticDir:str = os.path.join(os.getcwd(), "app", "static")

#Function to check if a filename is valid
def validateFilename(fName:str):
    if(is_valid_filename(filename=str(fName+".txt"))):
        return None
    else:
        raise HTTPException(status_code=400, detail="Not a valid name")

#Static CRUD check
@statRoute.get("/")
async def allHellos() ->list:
    if (not(os.path.exists(staticDir))):
        os.makedirs(staticDir)#make directory if it doesn't exist

    # Now check for the contents of staticDir
    helloList:list = os.listdir(staticDir)
    if(len(helloList)==0):
        raise HTTPException(status_code=404, detail="No greetings available at the moment")
    else:
        return [s.strip(".txt") for s in helloList] # strip out the .txt suffixes

#Request a specific greeting
@statRoute.get("/{filename}")#greet person by name and return their request body
async def helloGetter(filename:str)-> FileResponse:
    validateFilename(filename) #validate filename before proceeding
    targetFile:str = staticDir +"/"+ filename+".txt" #request params
    if (not(os.path.exists(staticDir))):
        os.makedirs(staticDir)#make directory if it doesn't exist
    if(os.path.exists(targetFile)):
        return FileResponse(targetFile) #return file to user
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#Post new file if name is unused
@statRoute.post("/{filename}")
async def helloPoster(filename:str, body:Textfile)-> str:
    validateFilename(filename) #validate filename before proceeding
    targetFile:str = filename+".txt" #request params
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
@statRoute.put("/{filename}")
async def helloPutter(filename:str, body:Textfile)-> str:
    validateFilename(filename) #validate filename before proceeding
    targetFile:str = staticDir +"/"+ filename+".txt" #request params
    if(os.path.exists(targetFile)):
        with open(targetFile, 'w', encoding='utf-8') as f:
            f.write(body.content)
        return ("Replaced "+ filename + " successfully!")
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#Add to specified file
@statRoute.patch("/{filename}")
async def helloPatcher(filename:str, body:Textfile)-> str:
    validateFilename(filename) #validate filename before proceeding
    targetFile:str = staticDir +"/"+ filename+".txt" #request params
    if(os.path.exists(targetFile)):
        with open(targetFile, 'a', encoding='utf-8') as f:
            f.write("\n" + body.content)
        return ("Added to "+ filename + " successfully!")
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#Delete specified file
@statRoute.delete("/{filename}")
async def helloRemover(filename:str)-> str:
    validateFilename(filename) #validate filename before proceeding
    targetFile:str = staticDir +"/"+ filename+".txt" #request params
    if(os.path.exists(targetFile)):
        os.remove(targetFile) #removed the file if it still
        return str(filename +" was successfully deleted!")
    else:
        raise HTTPException(status_code=404, detail="Item not found")