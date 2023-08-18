import os, json, asyncio #filepaths, JSONs, async requests
from motor.motor_asyncio import AsyncIOMotorClient #async connections to MongoDB

#MongoDB setup
MONGO_NAME:str = str(os.getenv("MONGODB_INITDB_DATABASE"))
MONGO_USER:str = str(os.getenv("MONGODB_INITDB_ROOT_USERNAME"))
MONGO_PASS:str = str(os.getenv("MONGODB_INITDB_ROOT_PASSWORD"))
MONGO_DOMAIN:str = str(os.getenv("MONGO_DOMAIN"))
portAsStr:str=str(os.getenv("MONGO_PORT"))
MONGO_PORT:int = int(portAsStr)
#Define MongoDB database URL
mongoTemp:str = "mongodb://{user}:{password}@{domain}:{port}/{dbname}?authSource={user}"
mongoURL:str = mongoTemp.format(
    user=MONGO_USER,
    password=MONGO_PASS,
    domain=MONGO_DOMAIN,
    port=MONGO_PORT,
    dbname=MONGO_NAME
)
print(mongoURL)
#Connect to MongoDB container:
mongoClient = AsyncIOMotorClient(mongoURL)
#Test function
async def testMongo():
    return await mongoClient.list_database_names()