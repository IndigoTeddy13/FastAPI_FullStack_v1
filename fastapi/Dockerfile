# Official Python 3.11.4 slim Docker image
FROM python:3.11.4-slim

# Set work directory
WORKDIR /code

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

VOLUME ["/code/app"]
# Install dependencies
COPY ./requirements.txt /code/requirements.txt 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy FastAPI project
COPY ./app /code/app