from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CreateTaskView.as_view(), name='task-create'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('<int:task_id>/edit/', views.EditTaskView.as_view(), name='task-update'),

]