# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /usr/src/app

# Copy the necessary files into the Docker image
COPY . .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the HTTP server
EXPOSE 8000

# Command to run the server when the container starts
CMD ["python", "agent_api.py"]
