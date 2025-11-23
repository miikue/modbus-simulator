# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file
COPY requirements.txt .

# Install system dependencies required for compilation
RUN apt-get update && apt-get install -y build-essential

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the simulator script
COPY simulator.py .

# Copy the version file into the image
COPY VERSION /app/version.txt

# Make port 5020 available to the world outside this container
EXPOSE 5020

# Run the simulator when the container launches
CMD ["python", "simulator.py"]
