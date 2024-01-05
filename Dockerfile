# Use the official Python image as the base image
FROM python:3.11-slim

# Create a working directory
WORKDIR /app

# Copy the project files to the working directory
COPY requirements.txt ./

# Create a virtual environment and activate it
RUN python3 -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="/app/venv/bin:${PATH}"

# Install the required dependencies
RUN pip install -r requirements.txt

# Copy the Flask application's code
COPY . .

# Expose the port for the Flask application
EXPOSE 8080

# Start the Flask application
CMD ["python", "app.py"]