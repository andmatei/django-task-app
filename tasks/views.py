from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View

from tasks.forms import EditTaskForm
from tasks.models import Task

class EditTask(View):
    def get(self, request):
        task_id = request.GET.get('task_id')
        
        task = None
        if task_id:
            task = Task.objects.get(id=task_id)
        
        form = EditTaskForm(instance=task)
        return render(request, 'tasks/edit_task.html', {'form': form})
    
    def post(self, request):
        task_id = request.POST.get('task_id')
        
        task = None
        if task_id:
            task = get_object_or_404(Task, id=task_id)

        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            return render(request, 'tasks/edit_task.html', {'form': form, 'errors': form.errors})
        
        
class Dashboard(View):
    def get(self, request):
        tasks = Task.objects.all()
        return render(request, 'tasks/dashboard.html', {'tasks': tasks})
    

class Index(View):
    def get(self, request):
        return render(request, 'tasks/index.html')
