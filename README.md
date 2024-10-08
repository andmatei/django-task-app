django-task-app
============

django-task-app is a Django app to conduct provides statistics for tasks.

Quick start
-----------

1. Run ``python manage.py migrate`` to create the models.

2. Start the development server with ``uvicorn task_app.asgi:application --host 0.0.0.0 --port 8000 --reload``.

3. Some functionalities of the website (such as the dashboard and all CRUD operations for tasks) are protected by a password (without the need for a username). To set this up, visit the admin page to configure a password. Create a user with the username ``user`` and the chosen password.

3. Visit ``/`` for the landing page. The other pages are protected by the chosen password.

5. Visit ``/tasks/dashboard`` for statistics about the tasks.

6. Visit ``/tasks/create`` to create a new task.
