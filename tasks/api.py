from ninja import NinjaAPI
import datetime
from tasks.models import Task
from django.core.paginator import Paginator
from django.http import JsonResponse

api = NinjaAPI()
@api.get("/tasks")
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

    context = {
        # 'page': page_obj,
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

