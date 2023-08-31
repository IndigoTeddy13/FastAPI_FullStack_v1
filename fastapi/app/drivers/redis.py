import os #environment

#Redis setup
#Format URL:
redisTemp:str = "redis://:{password}@{hostname}:{port}/{db_number}"
redisURL:str = redisTemp.format(
    password=str(os.getenv("REDIS_PASSWORD")),
    hostname=str(os.getenv("REDIS_DOMAIN")),
    port=str(os.getenv("REDIS_PORT")),
    db_number=0 #Start with DB0 for now
)