# TestingFastAPIv1
My first fullstack app with FastAPI as a backend. Two frontends (NGINX for HTML/CSS/JS, and a JS frontend framework). MongoDB as a database. Dockerized.

Currently WIP.

## Tech Stack
* Backend: FastAPI (an asynchronous REST framework for Python running on Uvicorn)
* Frontend 1: NGINX (serves prebuilt HTML, CSS, and JS)
* Frontend 2: Svelte (or maybe React, not sure yet)
* Database: MongoDB (Might ditch for MariaDB if I can't figure it out though)
* Reverse-Proxy via NGINX
* Runtime Environment: Docker

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
The backend, frontends, and DB are all mounted, as per docker-compose.yml.
