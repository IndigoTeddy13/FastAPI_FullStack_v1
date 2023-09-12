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
helloColl = mongoClient[FastAPI_DB]["Greetings"]

#Static markdown file route:
helloRoute = APIRouter()
staticDir:str = os.path.join(os.getcwd(), "app", "static")

#Function to check if a filename is valid
def validateFilename(fName:str):
    if(is_valid_filename(filename=str(fName+".md"))):
        return True
    raise HTTPException(status_code=400, detail="Not a valid name")

#Static CRUD check
@helloRoute.get("/")
async def allHellos():
    #Find a list of all greetings in the "Greetings" collection
    greetingsList:list = await queryManyToDict(helloColl.find({}, {"_id":0, "fName":1}))
    if (len(greetingsList) == 0):
        raise HTTPException(status_code=404, detail="No greetings are available at the moment.")
    #Return the list of available greetings
    outputList:list=[]
    for hi in greetingsList:
        outputList.append(hi.get("fName"))
    return outputList

#Request a specific greeting
@helloRoute.get("/{filename}")#greet person by name and return their request body
async def helloGetter(filename:str):
    validateFilename(filename) #validate filename before proceeding
    #Find a greeting if it exists:
    possibleGreeting = await helloColl.find_one({"fName":str(filename)}, {'_id': 0})
    if not(possibleGreeting):
        raise HTTPException(
            status_code=404,
            detail="Greeting {fName} doesn't currently exist.".format(fName=filename)
        )
    #Return the greeting as a file
    foundGreeting:MarkdownEntry = MarkdownEntry.model_validate(possibleGreeting)
    return Response(
        content=foundGreeting.content,
        headers={
            'Content-Disposition': 'inline; filename="{fn}.md"'.format(fn=foundGreeting.fName)
        },
        media_type="text/markdown"
    )

#Post new file if name is unused
@helloRoute.post("/{filename}")
async def helloPoster(filename:str, body:Markdown, request:Request):
    #Ensure the user is logged in first
    checkUser(request=request, needToken=True)
    #Write the file
    validateFilename(filename) #validate filename before proceeding
    #Find a greeting if it exists:
    possibleGreeting = await helloColl.find_one({"fName":str(filename)})
    if (possibleGreeting):
        raise HTTPException(
            status_code=403,
            detail="Greeting {fName} is already taken. Try again with another greeting name.".format(fName=filename)
        )
    #Post a new greeting
    newGreeting:MarkdownEntry = MarkdownEntry(
        fName=filename,
        content=body.content
    )
    await helloColl.insert_one(newGreeting.model_dump())
    return "Posted new greeting {fName} successfully!".format(fName=filename)

#Overwrite specified file
@helloRoute.put("/{filename}")
async def helloPutter(filename:str, body:Markdown, request:Request):
    #Ensure the user is logged in first
    checkUser(request=request, needToken=True)
    #Replace the file
    validateFilename(filename) #validate filename before proceeding
    #Find a greeting if it exists:
    possibleGreeting = await helloColl.find_one({"fName":str(filename)})
    if not(possibleGreeting):
        raise HTTPException(
            status_code=404,
            detail="Greeting {fName} doesn't currently exist.".format(fName=filename)
        )
    #Replace the greeting's content with the new content
    await helloColl.update_one(
        {'fName': filename},
        {'$set': {'content': body.content}}
    )
    return "Replaced greeting {fName} successfully!".format(fName=filename)

#Add to specified file
@helloRoute.patch("/{filename}")
async def helloPatcher(filename:str, body:Markdown, request:Request):
    #Ensure the user is logged in first
    checkUser(request=request, needToken=True)
    #Append to the file
    validateFilename(filename) #validate filename before proceeding
    #Find a greeting if it exists:
    possibleGreeting = await helloColl.find_one({"fName":str(filename)})
    if not(possibleGreeting):
        raise HTTPException(
            status_code=404,
            detail="Greeting {fName} doesn't currently exist.".format(fName=filename)
        )
    #Append to the greeting
    await helloColl.update_one(
        {'fName': filename},
        [{
            "$set": {"content": {
                "$concat":["$content", str("\n" + body.content)]
            }}
        }]
    )
    return "Appended to greeting {fName} successfully!".format(fName=filename)

#Delete specified file
@helloRoute.delete("/{filename}")
async def helloRemover(filename:str, request:Request):
    #Ensure the user is logged in first
    checkUser(request=request, needToken=True)
    #Remove the file
    validateFilename(filename) #validate filename before proceeding
    #Find a greeting if it exists:
    possibleGreeting = await helloColl.find_one({"fName":str(filename)})
    if not(possibleGreeting):
        raise HTTPException(
            status_code=404,
            detail="Greeting {fName} doesn't currently exist.".format(fName=filename)
        )
    #Remove the greeting
    await helloColl.delete_one({"fName":str(filename)})
    return "Deleted greeting {fName} successfully!".format(fName=filename)
