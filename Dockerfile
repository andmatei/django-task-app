FROM python:3.12-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

RUN pip install poetry

RUN poetry config virtualenvs.in-project true

COPY . .

RUN poetry install --no-dev && poetry check


EXPOSE 8000

RUN poetry shell

CMD ["python", "manage.py", "runserver"]