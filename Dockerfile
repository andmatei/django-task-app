# Build a Docker image for a Python application using Poetry

# Set base image (host OS)
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy application code into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.in-project true && poetry install --no-dev --no-root

# Expose port for the application
EXPOSE 8000

# Set default command to run the application
CMD ["poetry", "run", "uvicorn", "task_app.asgi:application", "--host", "0.0.0.0", "--port", "8000"]