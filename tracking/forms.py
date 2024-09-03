from django import forms
from tracking.models import Project, Task, Column, Comment

class CreateProjectForm(forms.ModelForm):
    class Meta():
        model = Project
        fields = ["name"]

class CreateCommentForm(forms.ModelForm):
    class Meta():
        model =Comment
        fields = ['text']

class CreateTaskForm(forms.ModelForm):
    class Meta():
        model = Task
        fields = ['name','text', 'status']