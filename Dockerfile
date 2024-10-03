FROM python:3.12-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

RUN pip install poetry

COPY . .

RUN poetry install --no-dev

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]