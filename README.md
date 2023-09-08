#  FastAPI_FullStack_v1
My first fullstack app. FastAPI is the backend. NGINX is the reverse proxy and static server. Svelte or another frontend framework (TBD). MongoDB is the primary database. Redis for session storage. Dockerized.
Currently WIP.

## Tech Stack
* Backend: FastAPI (an asynchronous REST framework for Python running on Uvicorn)
* Reverse-Proxy: NGINX (also serves static files)
* Frontend: Svelte (or maybe a different framework, TBD)
* Database: MongoDB (A NoSQL BSON Document-Store Database)
* Session Store: Redis (A NoSQL Key-Value Cache/Database that runs on active memory)
* Runtime Environment: Docker (Emulates multiple lightweight VMs to run processes as if they were on a network)

## Dockerization
To run as a docker container, open the main project directory and run the following commands, then go to http://localhost to visit the service. Entering http://localhost:3000 will load the Svelte frontend app instead of the NGINX frontend app.
```bash
docker-compose build
```
```bash
docker-compose up -d
```
Alternatively:
```bash
docker-compose up --build -d
```
To turn the container off:
```bash
docker-compose down
```

## Volumes
The backend, frontends, and DBs are all mounted, as per docker-compose.yml.
