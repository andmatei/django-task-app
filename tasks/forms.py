from tasks.models import Task
from django import forms


class EditTaskForm(forms.ModelForm):
    due_by = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = Task
        fields = "__all__"