FROM python:3.12-slim

WORKDIR /app

# Install system dependencies

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port (Railway will override this with its own PORT)
EXPOSE 7999

# Command to run the application using the PORT environment variable
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7999}"]
