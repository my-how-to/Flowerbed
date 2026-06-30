# Official Python runtime base image
FROM python:3.12-slim

# Install system dependencies
WORKDIR /app

# Remove the default Python bytecode generation (to avoid creating .pyc files)
ENV PYTHONDONTWRITEBYTECODE 1
# Set the environment variable to ensure that Python output is sent straight 
# to the terminal (stdout) without being buffered, which is useful for logging and debugging.
ENV PYTHONUNBUFFERED 1

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Expose port 8000 for the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
