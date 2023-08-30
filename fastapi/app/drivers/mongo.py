import os, pprint #environment, Cursor-to-Dictionary
from motor.motor_asyncio import AsyncIOMotorClient #async connections to MongoDB

#MongoDB setup
#Format URL:
mongoTemp:str = "mongodb://{user}:{password}@{domain}:{port}/{dbname}?authSource={user}"
mongoURL:str = mongoTemp.format(
    user=str(os.getenv("MONGODB_INITDB_ROOT_USERNAME")),
    password=str(os.getenv("MONGODB_INITDB_ROOT_PASSWORD")),
    domain=str(os.getenv("MONGO_DOMAIN")),
    port=str(os.getenv("MONGO_PORT")),
    dbname=str(os.getenv("MONGODB_INITDB_DATABASE"))
)
#Connect to MongoDB container:
mongoClient = AsyncIOMotorClient(mongoURL)

#Convert an inputted AsyncIOMotorCursor (such as a query) to a Python dictionary
async def queryToDict(c): # Input the query
    async for document in c:
        pprint.pprint(document) # The output is formatted into a dictionary

#Test function
async def testMongo():
    databases:list = await mongoClient.list_database_names() # list DBs
    selectedDB:str = databases[0]
    enteredDB = mongoClient[selectedDB] # Entered DB indexed 0
    collectionsInDB:list = await enteredDB.list_collection_names() # List collections in DB
    selectedCollection:str = collectionsInDB[0]
    enteredCollection= enteredDB[selectedCollection] #Entered collection indexed 0
    documentsCount:int = await enteredCollection.count_documents({})
    documentsInCollection = await queryToDict(enteredCollection.find({}))
    return{
        "databases":databases,
        "selectedDB":selectedDB,
        "collectionsInDB":collectionsInDB,
        "selectedCollection":selectedCollection,
        "documentsCount":documentsCount,
        "documentsInCollection":documentsInCollection
    }