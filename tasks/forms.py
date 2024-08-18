from tasks.models import Task
from django import forms


class EditTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = "__all__"