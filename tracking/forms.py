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
        widgets = {
            'text' : forms.Textarea(attrs={'class' : 'form-control'})
        }

class CreateTaskForm(forms.ModelForm):
    class Meta():
        model = Task
        fields = ['name','text', 'status']
        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'text' : forms.Textarea(attrs={'class' : 'form-control'}),
            'status' : forms.Select(choices=Task.STATUS_CHOICES,attrs={'class' : 'form-control'})
        }

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
        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control'})
        }


        