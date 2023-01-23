# Use an official Ubuntu runtime as the base image
FROM ubuntu:20.04
FROM python:36
# Update the package manager
RUN apt-get update -y

# Install python3 and pip3
RUN apt-get install -y python3 python3-pip

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Copy the application code into the container
COPY . .

# Make port 80 available to the world outside this container
EXPOSE 8080

# # Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["python3","-b","0.0.0.8080", "app:app","--workers=5"]
