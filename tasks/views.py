import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from tasks.forms import EditTaskForm
from tasks.models import Task

class CreateTaskView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditTaskForm()
        return render(request, 'tasks/edit_task.html', {'form': form})
    
    def post(self, request):
        form = EditTaskForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, 'tasks/edit_task.html', {'form': form, 'errors': form.errors})
        

class EditTaskView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = EditTaskForm(instance=task)
        return render(request, 'tasks/edit_task.html', {'form': form})


class DeleteTaskView(LoginRequiredMixin, View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        task.delete()
        return HttpResponseRedirect(reverse('dashboard'))
    

class EditTaskView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = EditTaskForm(instance=task)
        return render(request, 'tasks/edit_task.html', {'form': form})
    
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, 'tasks/edit_task.html', {'form': form, 'errors': form.errors})

    
class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        days = request.GET.get('days', 30)

        now = datetime.datetime.now()
        delta = datetime.timedelta(days=days)

        start_time = now
        end_time = now + delta

        all_tasks = Task.objects.all()
        
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
            'tasks': all_tasks,
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

        return render(request, 'tasks/dashboard.html', context)
    

class IndexView(View):
    def get(self, request):
        return render(request, 'tasks/index.html')
