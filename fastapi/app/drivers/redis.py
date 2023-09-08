import os #environment

#Redis setup
#Format URL:
redisURL:str = "redis://:{password}@{hostname}:{port}/{db_number}".format(
    password=str(os.getenv("REDIS_PASSWORD")),
    hostname=str(os.getenv("REDIS_DOMAIN")),
    port=str(os.getenv("REDIS_PORT")),
    db_number=0 #Start with DB0 for now
)