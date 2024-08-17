from django import forms

class TaskForm(forms.Form):
    user_email = forms.EmailField()
    task = forms.CharField(max_length=200)
    due_by = forms.DateTimeField()
    priority = forms.IntegerField()
    is_urgent = forms.BooleanField(initial=False)