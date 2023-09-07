# Use the official Python image as the base image
FROM --platform=linux/amd64 python:3.8

RUN apt-get update && apt-get install -y libsndfile1

# Set the working directory inside the container
WORKDIR /app

COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install -r dependencies.txt

# Expose the port that your Flask app will run on
EXPOSE 8080

# Define the command to run your Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "server:app"]