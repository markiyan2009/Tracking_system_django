from django import forms
from tracking.models import Project, Task, Column, Comment

class CreateProjectForm(forms.ModelForm):
    class Meta():
        model = Project
        fields = ["name"]
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control-plaintext'})
        }

class CreateCommentForm(forms.ModelForm):
    class Meta():
        model =Comment
        fields = ['text']

class CreateTaskForm(forms.ModelForm):
    class Meta():
        model = Task
        fields = ['name','text', 'status']

class TaskFilterForm(forms.Form):
    STATUS_CHOICES = [
        ("", "All"),
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Status")
    

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)
        self.fields["status"].widget.attrs.update({"class": "form-control"})

class CreateColumnForm(forms.ModelForm):
    class Meta():
        model = Column
        fields = ['name']
        