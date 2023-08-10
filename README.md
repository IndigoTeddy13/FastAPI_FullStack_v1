# TestingFastAPIv1
My first attMy first fullstack app with FastAPI as a backend. Two frontends (NGINX for HTML/CSS/JS, and Svelte). MongoDB as a database. Dockerized. empt at building a fullstack app for FastAPI.

## Tech Stack
* Backend: FastAPI
* Frontend: Svelte (or maybe React, not sure yet)
* DB: MongoDB
* Reverse-Proxy (might remove this if I don't need it): Traefik
* Runtime Environment: Docker

## Dockerization
To run as a docker container, open main project directory and run the following commands, then go to http://localhost to visit the service:
```bash
docker-compose build
```
```bash
docker-compose up -d
```
To turn the container off:
```bash
docker-compose down
```

## Mounts
I already mounted the backend (app folder). Planning to mount the compilation target of the frontend. Also mounting MongoDB to ensure the content doesn't get lost when I close the image.
