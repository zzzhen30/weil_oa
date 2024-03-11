# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# # Copy the current directory contents into the container at /app
#  Dockerfile in the same directory as other application code
COPY . .

# needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 1319 available to the world outside this container
EXPOSE 1319


# Define environment variable
ENV FLASK_APP=app.py


# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0", "--port=1319"]
