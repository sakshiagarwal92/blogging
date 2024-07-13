# Use the official Python image as a base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /code/

# Install the required dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /code/

# Ensure the entrypoint script is executable
RUN chmod +x /code/entrypoint.sh

# Specify the command to run on container start
CMD ["./entrypoint.sh"]
