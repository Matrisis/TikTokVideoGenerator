# Use an official Python runtime as the parent image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents (where the Dockerfile lives) to the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg