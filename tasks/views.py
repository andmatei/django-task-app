import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from tasks.forms import EditTaskForm
from tasks.models import Task

class CreateTaskView(LoginRequiredMixin, View):
    def get(self, request):
        form = EditTaskForm()
        return render(request, 'tasks/edit_task.html', {'form': form})
    

class EditTaskView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        form = EditTaskForm(instance=task)
        return render(request, 'tasks/edit_task.html', {'form': form})
    
class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tasks/dashboard.html')

