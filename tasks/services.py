from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from .models import Task
from django.shortcuts import get_object_or_404

async def serv_get_paginated_tasks(start_time, end_time, page_number, tasks_per_page):
    all_tasks = await sync_to_async(list)(
        Task.objects.filter(due_by__range=[start_time, end_time]).values()
    )
    paginator = Paginator(all_tasks, tasks_per_page)
    page_obj = await sync_to_async(paginator.get_page)(page_number)
    return page_obj

async def serv_update_task(task_id, payload):
    task = await sync_to_async(get_object_or_404)(Task, id=task_id)
    task.user_email = payload.user_email
    task.task = payload.task
    task.due_by = payload.due_by
    task.priority = payload.priority
    task.is_urgent = payload.is_urgent
    await sync_to_async(task.save)()
    return task