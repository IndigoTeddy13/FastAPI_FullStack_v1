#Imports
import os #filepaths
from fastapi import FastAPI, HTTPException #FastAPI stuff
from fastapi.responses import FileResponse # send text files to users
#Personal imports
from .pydModels import *

#Static text file route:
statRoute = FastAPI()

#Static CRUD check

#Request a specific greeting
@statRoute.get("/{filename}")#greet person by name and return their request body
async def helloGetter(filename:str)-> FileResponse:
    targetFile:str = os.path.join(os.getcwd(), "app", "static") +"/"+ filename+".txt" #request params
    if(os.path.exists(targetFile)):
        return FileResponse(targetFile) #return file to user
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#Post new file if name is unused
@statRoute.post("/{filename}")
async def helloPoster(filename:str, body:Textfile)-> str:
    targetFile:str = filename+".txt" #request params
    targetPath:str = os.path.join(os.getcwd(), "app", "static")
    if (not(os.path.exists(targetPath))):
        os.makedirs(targetPath)#make directory if it doesn't exist
    newPath:str = targetPath+"/"+targetFile
    if(not(os.path.exists(newPath))):
        with open(newPath, 'w', encoding='utf-8') as f:
            f.write(body.content)
        return ("Posted "+ filename +" successfully!")
    else:
        raise HTTPException(status_code=404, detail="Item already exists")

#Overwrite specified file
@statRoute.put("/{filename}")
async def helloPutter(filename:str, body:Textfile)-> str:
    targetFile:str = os.path.join(os.getcwd(), "app", "static") +"/"+ filename+".txt" #request params
    if(os.path.exists(targetFile)):
        with open(targetFile, 'w', encoding='utf-8') as f:
            f.write(body.content)
        return ("Replaced "+ filename + " successfully!")
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#Add to specified file
@statRoute.patch("/{filename}")
async def helloPatcher(filename:str, body:Textfile)-> str:
    targetFile:str = os.path.join(os.getcwd(), "app", "static") +"/"+ filename+".txt" #request params
    if(os.path.exists(targetFile)):
        with open(targetFile, 'a', encoding='utf-8') as f:
            f.write("\n" + body.content)
        return ("Added to "+ filename + " successfully!")
    else:
        raise HTTPException(status_code=404, detail="Item not found")

#Delete specified file
@statRoute.delete("/{filename}")
async def helloRemover(filename:str)-> str:
    targetFile:str = os.path.join(os.getcwd(), "app", "static") +"/"+ filename+".txt" #request params
    if(os.path.exists(targetFile)):
        os.remove(targetFile) #removed the file if it still
        return str(filename +" was successfully deleted!")
    else:
        raise HTTPException(status_code=404, detail="Item not found")