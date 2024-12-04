# Using a lightweight Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app-frontend

# Copy the current directory contents into the container at /app
COPY . /app-frontend

# Install dependencies
RUN pip install -r requirements.txt

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run app.py when the container launches
CMD ["python", "main.py"]