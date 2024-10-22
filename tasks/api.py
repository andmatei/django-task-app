# Core imports for Ninja API
from ninja import NinjaAPI
from ninja import Query
from ninja.security import django_auth
from ninja.pagination import paginate

# Django utilities and HTTP handling
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponse
from django.forms.models import model_to_dict


# Asynchronous utilities
from asgiref.sync import sync_to_async
import asyncio

# Importing models
from tasks.models import Task

# Importing schemas
from .schemas import *

# Date and time utilities
import datetime
# Services
from .services import serv_get_paginated_tasks
from .services import serv_update_task

api = NinjaAPI(auth=sync_to_async(django_auth)) # Maybe this is fine but feels so wrong...

@api.get("/tasks", response=TaskPageDataSchema)
async def get_tasks(request, query: TaskQueryParams = Query()):
    now = timezone.now()
    delta = datetime.timedelta(days=query.days_time_span)
    end_time = now + delta

    tasks = await serv_get_paginated_tasks(now,end_time, query.page_number, query.tasks_per_page, query.priority_filter)

    processed_tasks = [
        {
            **task,
            'due_by': task['due_by'].date()  # Convert datetime to date
        }
        for task in tasks.object_list
    ]

    page_data = {
        'tasks': processed_tasks,
        'number': tasks.number,
        'num_pages': tasks.paginator.num_pages,
        'has_next': tasks.has_next(),
        'has_previous': tasks.has_previous(),
    }

    return page_data


@api.get("/tasks/{task_id}", response=TaskSchema)
async def get_task(request, task_id: int):
    task = await sync_to_async(get_object_or_404)(Task, id=task_id)
    task_data = {
        'id': task.id,
        'user_email': task.user_email,
        'task': task.task,
        'due_by': task.due_by,
        'priority': task.priority,
        'is_urgent': task.is_urgent
    }
    return task_data


@api.put("/tasks/{task_id}", response={200: None, 400: None})
async def update_task(request, task_id: int, payload: TaskIn):
    updated_task = await serv_update_task(task_id, payload)
    return JsonResponse(data=model_to_dict(updated_task), status=200)

@api.delete("/tasks/{task_id}", response={200: None, 404: None})
async def delete_task(request, task_id: int):
    task = await sync_to_async(get_object_or_404)(Task, id=task_id)
    await sync_to_async(task.delete)()
    return HttpResponse(status=200)


@api.post("/tasks", response={200: None, 201: None, 400: None})
async def create_task(request, payload: TaskIn):
    try:
        task = await sync_to_async(Task.objects.create)(**payload.dict())
        return JsonResponse(data=model_to_dict(task), status=201)
    except Exception as e:
        print(e) #debug
        return JsonResponse(data={"message": str(e)}, status=400)