# Base image
FROM python:3.10-slim

# Define workdir
WORKDIR /app-backend

# Copy files from app folder to current workdir
COPY ./app .

COPY requirements.txt /app-backend

# Install dependencies
RUN pip install -r /app-backend/requirements.txt

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]