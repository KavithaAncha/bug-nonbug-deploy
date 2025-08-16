# Use Python base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy everything inside the app folder
COPY app/ /app/

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]

COPY requirements.txt .
