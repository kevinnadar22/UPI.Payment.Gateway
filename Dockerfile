# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1  # Ensures that Python output is sent straight to terminal without buffering
ENV PYTHONDONTWRITEBYTECODE 1  # Prevents Python from writing .pyc files to disk

# Set the working directory in the container
WORKDIR /app

# Copy only requirements file first (for better build caching)
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Set environment variable for port (default 8000)
ENV PORT=8000

# Expose the port to be accessible externally
EXPOSE $PORT

# Use gunicorn as the production server
CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "app:app", "--workers=4", "--threads=2", "--timeout=120", "--log-level=info"]
