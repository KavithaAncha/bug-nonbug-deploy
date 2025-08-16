# Use Python base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the application code (including model and templates)
COPY app/ /app/

# Copy the requirements.txt from the root of your repo
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# Expose port (optional, but good practice)
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
