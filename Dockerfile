FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (includes model and templates)
COPY app/ app/

# Default env vars
ENV MODEL_PATH=/app/model/bug_classifier_pipeline.pkl
ENV PORT=5000

EXPOSE 5000

# Run with Gunicorn (production WSGI server)
CMD ["python", "-m", "app.app"]
