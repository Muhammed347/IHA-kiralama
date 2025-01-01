# Base image
FROM python:3.10-slim

# Install build dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     tzdata \
#     && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port 8000 for Django development server
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
