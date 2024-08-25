from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from tracking.models import Project, Column, Task
from tracking.mixins import UserIsAssignedMixin
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from tracking.forms import CreateProjectForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ProjectsListview(ListView):
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
        
        context['columns'] = columns
        
        return context
    
    
class CreateProjectView(LoginRequiredMixin,CreateView):
    model = Project
    template_name="tracking/add_project.html"
    form_class=CreateProjectForm
    success_url = reverse_lazy('projects')
    
    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

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