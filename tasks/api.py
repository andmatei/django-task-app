# External Libraries
from ninja import NinjaAPI
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

@api.get("/tasks", response=TaskPageDataSchema)
def get_tasks(request, query: TaskQueryParams = Query()):
    now = timezone.now() # switch to timezone.now 
    delta = datetime.timedelta(days=query.days)

    start_time = now
    end_time = now + delta

    all_tasks = Task.objects.all()

    paginator = Paginator(all_tasks, query.tasks_per_page)
    page_obj = paginator.get_page(query.page_number)

    # Filter tasks by due date
    upcoming_tasks = Task.objects.filter(due_by__range=[start_time, end_time])
    
    # Filter tasks by urgency
    urgent_tasks = upcoming_tasks.filter(is_urgent=True)
    
    # Group tasks by priority
    low_priority_tasks = upcoming_tasks.filter(priority=1)
    medium_priority_tasks = upcoming_tasks.filter(priority=2)
    high_priority_tasks = upcoming_tasks.filter(priority=3)

    dates = {
        'low_priority': [0 for _ in range(query.days)],
        'medium_priority': [0 for _ in range(query.days)],
        'high_priority': [0 for _ in range(query.days)],
        'total': [0 for _ in range(query.days)],
    }
    for task in upcoming_tasks:
        date = task.due_by.date()
        index = (date - now.date()).days

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
            for task in page_obj.object_list.values()
        ]
    }

    context = {
        'page': page_data,
        'start_date': start_time.date(),
        'end_date': end_time.date(),
        'stats': {
            'counts': {
                'urgent': urgent_tasks.count(),
                'low_priority': low_priority_tasks.count(),
                'medium_priority': medium_priority_tasks.count(),
                'high_priority': high_priority_tasks.count(),
                'total': upcoming_tasks.count(),
            },
            'dates': dates,
        },
    }
    return context


@api.put("/tasks/{task_id}",response={200: dict, 400: dict})
def update_task(request, task_id: int, payload: UpdateTaskSchema):
    task = get_object_or_404(Task, id=task_id)

    task.user_email = payload.user_email
    task.task = payload.task
    task.due_by = payload.due_by
    task.priority = payload.priority
    task.is_urgent = payload.is_urgent

    task.save()

    return JsonResponse(data={"message": "Task updated successfully"}, status=200)


@api.delete("/tasks/{task_id}", response={200: dict, 404: dict})
def delete_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return {"message": "Task deleted successfully"}

@api.post("/tasks", response={200: dict, 201: dict, 400: dict})
def create_task(request, payload: TaskSchema):
    task = Task.objects.create(**payload.dict())
    return {"message": "Task created successfully"}
