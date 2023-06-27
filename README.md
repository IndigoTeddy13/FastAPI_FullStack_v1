# TestingFastAPIv1
My first attempt at building a fullstack app for FastAPI. Not sure how I'll implement the frontend yet.

To run directly, open main project directory, install mandatory pip packages, and run the uvicorn command, then go to http://localhost:3000 to visit the service:
```bash
pip install --no-cache-dir --upgrade -r requirements.txt
```
```bash
uvicorn app.main:app --port 3000
```
Optional (to reload automatically after saving changes):
```bash
uvicorn app.main:app --port 3000 --reload
```

To run as a docker container, open main project directory and run the following commands, then go to http://localhost:3000 to visit the service:
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