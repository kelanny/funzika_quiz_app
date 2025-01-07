# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev build-essential && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Gunicorn will use
EXPOSE 8000

# Start the app using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
