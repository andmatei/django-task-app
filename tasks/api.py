from ninja import NinjaAPI
import datetime
from tasks.models import Task
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from tasks.forms import EditTaskForm
from django.http import QueryDict
from ninja.security import django_auth
import json


api = NinjaAPI()

@api.get("/tasks", auth=django_auth)
def get_tasks(request):
    days = request.GET.get('days', 30)
    tasks_per_page = request.GET.get('tasks_per_page', 10)
    page_number = request.GET.get('page', 1)

    now = datetime.datetime.now()
    delta = datetime.timedelta(days=days)

    start_time = now
    end_time = now + delta

    all_tasks = Task.objects.all()

    paginator = Paginator(all_tasks, tasks_per_page)
    page_obj = paginator.get_page(page_number)

    # Filter tasks by due date
    upcoming_tasks = Task.objects.filter(due_by__range=[start_time, end_time])
    
    # Filter tasks by urgency
    urgent_tasks = upcoming_tasks.filter(is_urgent=True)
    
    # Group tasks by priority
    low_priority_tasks = upcoming_tasks.filter(priority=1)
    medium_priority_tasks = upcoming_tasks.filter(priority=2)
    high_priority_tasks = upcoming_tasks.filter(priority=3)

    dates = {
        'low_priority': [0 for _ in range(days)],
        'medium_priority': [0 for _ in range(days)],
        'high_priority': [0 for _ in range(days)],
        'total': [0 for _ in range(days)],
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
        'tasks': list(page_obj.object_list.values())
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
    return JsonResponse(context)

@api.put("/tasks/{task_id}", auth=django_auth)
def update_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id)
    task_data = QueryDict(request.body.decode("utf-8"))
    
    form = EditTaskForm(task_data, instance=task)
    # Check if the form is valid
    if form.is_valid():
        # Save the updated task
        form.save()
        # Return a success message
        return JsonResponse({"message": "Task updated successfully"})
    else:
        # Return the form errors if the form is not valid
        return JsonResponse({"errors": form.errors}, status=400)

    


@api.delete("/tasks/{task_id}", auth=django_auth)
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return JsonResponse({'message': 'Task deleted successfully'})

@api.post("/tasks", auth=django_auth) # TO ADD
def create_task(request):
    form = EditTaskForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'Task created successfully'})
    else:
        return JsonResponse({'errors': form.errors})