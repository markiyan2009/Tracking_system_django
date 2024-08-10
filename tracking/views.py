from django.shortcuts import render
from tracking.models import Project, Column, Task
from django.views.generic import ListView, DetailView, CreateView

# Create your views here.
class ProjectsListview(ListView):
    model = Project
    template_name = "tracking/projects.html"
    context_object_name = "projects"

class ProjectDetailView(DetailView):
    model = Project
    template_name = "tracking/project.html"