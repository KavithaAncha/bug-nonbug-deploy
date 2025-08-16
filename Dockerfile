# Use Python base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy the app folder into the container
COPY app/ /app/

# Copy requirements.txt from project root into container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on (optional)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
