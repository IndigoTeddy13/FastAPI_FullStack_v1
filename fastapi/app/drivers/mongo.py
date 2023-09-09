import os, pprint #environment, Cursor-to-Dictionary
from motor.motor_asyncio import AsyncIOMotorClient #async connections to MongoDB

#Store FastAPI_DB for future use
FastAPI_DB:str = str(os.getenv("MONGODB_INITDB_DATABASE"))

#MongoDB setup
#Format URL:
mongoURL:str = "mongodb://{user}:{password}@{domain}:{port}/{dbname}?authSource={user}".format(
    user=str(os.getenv("MONGODB_INITDB_ROOT_USERNAME")),
    password=str(os.getenv("MONGODB_INITDB_ROOT_PASSWORD")),
    domain=str(os.getenv("MONGO_DOMAIN")),
    port=str(os.getenv("MONGO_PORT")),
    dbname=FastAPI_DB
)
#Connect to MongoDB container:
mongoClient = AsyncIOMotorClient(mongoURL)

#Convert an inputted AsyncIOMotorCursor (such as a query) to a Python dictionary
async def queryManyToDict(c): # Input the query
    myList:list = []
    async for document in c:
        myList.append(document)
    return myList

#Test function
async def testMongo():
    try:
        await mongoClient["admin"].command('ping')
        return ("Pinged your deployment. You have successfully connected to MongoDB!")
    except Exception as e:
        return(e)