from django import forms
from tracking.models import Project, Task, Column

class CreateProjectForm(forms.ModelForm):
    class Meta():
        model = Project
        fields = ["name"]