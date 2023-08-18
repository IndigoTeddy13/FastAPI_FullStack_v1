import os, json, asyncio #filepaths, JSONs, async requests
from motor.motor_asyncio import AsyncIOMotorClient #async connections to MongoDB
from sqlalchemy import create_engine, MetaData

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

###
###
###

#MariaDB setup
MARIA_NAME:str = str(os.getenv("MARIADB_DATABASE"))
MARIA_USER:str = str(os.getenv("MARIA_USER"))
MARIA_PASS:str = str(os.getenv("MARIADB_ROOT_PASSWORD"))
MARIA_DOMAIN:str = str(os.getenv("MARIA_DOMAIN"))
portAsStr= str(os.getenv("MARIA_PORT"))
MARIA_PORT:int = int(portAsStr)
#Define MariaDB database URL
#"mysql+pymysql://admin:1234@localhost:3306/dev"
mariaTemp:str = "mysql+pymysql://{user}:{password}@{domain}:{port}/{dbname}?charset=utf8"
mariaURL:str = mariaTemp.format(
    user=MARIA_USER,
    password=MARIA_PASS,
    domain=MARIA_DOMAIN,
    port=MARIA_PORT,
    dbname=MARIA_NAME
)
print(mariaURL)
#Connect to MariaDB container:
engine = create_engine(mariaURL)
metadata = MetaData()
conn = engine.connect()
#Test function
async def testMaria():
    return metadata.tables.keys()
