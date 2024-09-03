from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from tracking.models import Project, Column, Task, Comment
from tracking.mixins import UserIsAssignedMixin
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib import messages
from django.contrib.auth.models import User
from tracking.forms import CreateProjectForm, CreateCommentForm, CreateTaskForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect

# Create your views here.
class ProjectsListview(ListView):
    model = Project
    template_name = "tracking/projects.html"
    context_object_name = "projects"


class ProjectDetailView(LoginRequiredMixin, DetailView):
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

class CustomLoginView(LoginView):
    template_name = 'tracking/login.html'
    redirect_authenticated_user = True

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tracking/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CreateCommentForm()
        context['comments'] = Comment.objects.filter(task = context['task']).all()
        return context
    
    def post(self, request, *args, **kwargs):
        comment_form = CreateCommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.owner = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('task_detail', pk=comment.task.pk)
    
class TaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = "done"
        task.save()
        return HttpResponseRedirect(reverse_lazy("projects"))

    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(Task, pk=task_id)
    

class CustomLogoutView(LogoutView):
    next_page="login"

class RegisterView(CreateView):
    template_name = 'tracking/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

#Не робить
class CreateTaskView(CreateView):
    template_name = 'tracking/add_task.html'
    form_class = CreateTaskForm
    success_url = reverse_lazy('projects')
    def form_valid(self, form):
        form.instance.column = self
        return redirect(self.get_success_url())
    