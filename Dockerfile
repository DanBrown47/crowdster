# Use an official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt ./

# Install the required packages using pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the container
COPY . ./

# Expose the default Flask port
EXPOSE 5000

# Define the command to run the Flask application
CMD ["flask", "run","--host=0.0.0.0"]