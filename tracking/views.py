from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from tracking.models import Project, Column, Task
from tracking.mixins import UserIsAssignedMixin
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.contrib.auth import authenticate, login

# Create your views here.
class ProjectsListview(UserIsAssignedMixin,ListView):
    model = Project
    template_name = "tracking/projects.html"
    context_object_name = "projects"
    def get_queryset(self):
        
        return Project.objects.filter(owner = self.request.user).all()

class ProjectDetailView(UserIsAssignedMixin,DetailView):
    model = Project
    template_name = "tracking/project.html"
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        project = context['project']
        

        columns = project.column_set.all()
        
        columns_with_tasks = []
        for column in columns:
            tasks = column.task_set.all()
            columns_with_tasks.append({
                'column': column,
                'tasks': tasks,
            })
        
           
        context['columns'] = columns
        context['columns_with_tasks'] = columns_with_tasks
        
        return context
def login_view(request):
    
    if request.method == "POST":
            
        
            
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            print(1234)
            return redirect("projects")
        else:
            
            messages.error(request,message="Wrong username or password")

    
    return render(request,template_name="tracking/login.html")