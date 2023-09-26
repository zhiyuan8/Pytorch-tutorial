# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster

# This is to create a new folder in image!
WORKDIR /app

# Copy the requirements.txt to requirements.txt
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy all the source code to the created app folder.
COPY . .
# CMD refers to the command!
CMD [ "python3", "app.py"]