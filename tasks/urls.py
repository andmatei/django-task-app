from django.urls import path
from . import views

urlpatterns = [
    path('edit/', views.EditTask.as_view(), name='edit_task'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('', views.Index.as_view(), name='index'),
]