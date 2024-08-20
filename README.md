============
django-task-app
============

django-task-app is a Django app to conduct provides statistics for tasks.

Quick start
-----------

1. Run ``python manage.py migrate`` to create the models.

2. Start the development server with ``python manage.py runserver``.

3. Visit the admin page to configure a password for accessing all the functionalities of the website. Create a user with the username ``user`` and the chosen password.

3. Visit ``/`` for the landing page. The other pages are protected by the chosen password.

5. Visit ``/tasks/dashboard`` for statistics about the tasks.

6. Visit ``/tasks/create`` to create a new task.