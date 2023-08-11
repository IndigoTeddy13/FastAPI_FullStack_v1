# TestingFastAPIv1
My first fullstack app with FastAPI as a backend. Two frontends (NGINX for HTML/CSS/JS, and Svelte). MongoDB as a database. Dockerized.

## Tech Stack
* Backend: FastAPI
* Frontend 1: NGINX (serve HTML, CSS, and JS)
* Frontend 2: Svelte (or maybe React, not sure yet)
* Database: MongoDB
* Reverse-Proxy (might remove this if I don't need it): Traefik
* Runtime Environment: Docker

## Dockerization
To run as a docker container, open the main project directory and run the following commands, then go to http://localhost to visit the service. Entering http://localhost:3000 will load the Svelte frontend app instead of the NGINX frontend app.
Windows:
```bash
bash run.sh
```
Linux:
```bash
./run.sh
```
To turn the container off:
```bash
docker-compose down
```

## Volumes
The backend, frontends, and DB are all mounted, as per docker-compose.yml.
