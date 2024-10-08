# Build a Docker image for a Python application using Poetry

# Set base image (host OS)
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install Poetry
RUN pip install poetry

# Set Poetry configuration to create virtualenv in project directory
RUN poetry config virtualenvs.in-project true

# Copy application code into the container
COPY . /app

# Install application dependencies
RUN poetry install --no-dev --no-root

# Expose port for the application
EXPOSE 8000

# Set default command to run the application
CMD ["poetry", "run", "python", "manage.py", "runserver", "--verbosity", "3", "0.0.0.0:8000"]