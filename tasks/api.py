# External Libraries
from ninja import NinjaAPI
from asgiref.sync import sync_to_async
import asyncio
from ninja import Query
from .schemas import *
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ninja.security import django_auth

# Django
from django.utils import timezone

# Models
from tasks.models import Task

# Utilities
import datetime

api = NinjaAPI(auth=django_auth)

@api.get("/tasks", response=TaskPageDataSchema, auth=None)
async def get_tasks(request, query: TaskQueryParams = Query()):
    now = timezone.now()  # This is fine as it is
    delta = datetime.timedelta(days=query.days)

    start_time = now
    end_time = now + delta

    # Wrap synchronous ORM calls
    all_tasks = await sync_to_async(list)(Task.objects.all().values())
    paginator = Paginator(all_tasks, query.tasks_per_page)
    page_obj = await sync_to_async(paginator.get_page)(query.page_number)

    # Filter tasks by due date
    upcoming_tasks = await sync_to_async(list)(Task.objects.filter(due_by__range=[start_time, end_time]))    # Filter tasks by urgency
    urgent_tasks = [task for task in upcoming_tasks if task.is_urgent]

    # Group tasks by priority
    low_priority_tasks = [task for task in upcoming_tasks if task.priority == 1]
    medium_priority_tasks = [task for task in upcoming_tasks if task.priority == 2]
    high_priority_tasks = [task for task in upcoming_tasks if task.priority == 3]

    dates = {
        'low_priority': [0 for _ in range(query.days)],
        'medium_priority': [0 for _ in range(query.days)],
        'high_priority': [0 for _ in range(query.days)],
        'total': [0 for _ in range(query.days)],
    }
    for task in upcoming_tasks:
        date = task.due_by.date()
        index = (date - now.date()).days
        if 0 <= index < query.days:
            dates['total'][index] += 1
            if task.priority == 1:
                dates['low_priority'][index] += 1
            elif task.priority == 2:
                dates['medium_priority'][index] += 1
            elif task.priority == 3:
                dates['high_priority'][index] += 1


    page_data = {
        'number': page_obj.number,
        'num_pages': page_obj.paginator.num_pages,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'tasks': [
            {
                **task,
                'due_by': task['due_by'].date()  # Convert datetime to date
            }
            for task in page_obj.object_list
        ]
    }

    context = {
        'page': page_data,
        'start_date': start_time.date(),
        'end_date': end_time.date(),
        'stats': {
            'counts': {
                'urgent': len(urgent_tasks),
                'low_priority': len(low_priority_tasks),
                'medium_priority': len(medium_priority_tasks),
                'high_priority': len(high_priority_tasks),
                'total': len(upcoming_tasks),
            },
            'dates': dates,
        },
    }
    return context


@api.put("/tasks/{task_id}", response={200: dict, 400: dict}, auth=None)
async def update_task(request, task_id: int, payload: UpdateTaskSchema):
    task = await sync_to_async(get_object_or_404)(Task, id=task_id)

    task.user_email = payload.user_email
    task.task = payload.task
    task.due_by = payload.due_by
    task.priority = payload.priority
    task.is_urgent = payload.is_urgent

    await sync_to_async(task.save)()  # task.save()

    return JsonResponse(data={"message": "Task updated successfully"}, status=200)

@api.delete("/tasks/{task_id}", response={200: dict, 404: dict}, auth = None)
async def delete_task(request, task_id: int):
    task = await sync_to_async(get_object_or_404)(Task, id=task_id)
    await sync_to_async(task.delete)()
    return JsonResponse(data={"message": "Task deleted successfully"}, status=200)

@api.post("/tasks", response={200: dict, 201: dict, 400: dict}, auth=None)
async def create_task(request, payload: CreateTaskSchema):
    try:
        task = await sync_to_async(Task.objects.create)(**payload.dict())
        return JsonResponse(data={"message": "Task created successfully"}, status=201)
    except Exception as e:
        return JsonResponse(data={"message": str(e)}, status=400)