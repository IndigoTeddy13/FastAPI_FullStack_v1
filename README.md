# TestingFastAPIv1
My first attempt at building a fullstack app for FastAPI. Not sure how I'll implement the frontend yet.

#LocalHosting
To run backend directly, open main project directory, install mandatory pip packages, and run the uvicorn command, then go to http://localhost to visit the service:
```bash
pip install --no-cache-dir --upgrade -r requirements.txt
```
```bash
uvicorn api.main:app --port 80
```
Optional (to reload automatically after saving changes):
```bash
uvicorn api.main:app --port 80 --reload
```
After activating the backend, open an HTML file in the browser to get started. Currently might not work on some browsers.

#Dockerization
To run as a docker container, open main project directory and run the following commands, then go to http://fastapi.localhost to visit the service:
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