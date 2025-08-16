FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy all contents from the app folder into /app
COPY app/ /app/

# Copy requirements.txt from repo root into /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app runs on
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
