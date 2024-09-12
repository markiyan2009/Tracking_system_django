from typing import Any, Dict
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect, get_object_or_404
from tracking.models import Project, Column, Task, Comment
from tracking.mixins import UserIsAssignedTaskMixin, UserIsAssignedCommentkMixin
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.models import User
from tracking.forms import CreateProjectForm, CreateCommentForm, CreateTaskForm, TaskFilterForm, CreateColumnForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from random import randint



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

        status = self.request.GET.get("status", "")
        for column in columns:
            if status:
            
                column.filtered_tasks = column.tasks.filter(status=status)
            else:
                column.filtered_tasks = column.tasks.all()

        context['columns'] = columns 
        
        
        context["form"] = TaskFilterForm(self.request.GET)
        
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
        return HttpResponseRedirect(reverse_lazy("task_detail", kwargs={'pk': task.pk}))

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


class CreateTaskView(CreateView):
    template_name = 'tracking/add_task.html'
    form_class = CreateTaskForm
    
    def form_valid(self, form):
        column_id = self.kwargs['column_id']
        column = get_object_or_404(Column, id=column_id)
        form.instance.column = column
        return super().form_valid(form)
    def get_success_url(self) -> str:
        return reverse_lazy('project',  kwargs={'pk': self.object.column.project.pk})
    
class UpdateCommentView(UserIsAssignedCommentkMixin,UpdateView):
    model = Comment
    template_name = 'tracking/update_comment.html'
    fields= ['text']
    

    def form_valid(self, form: BaseModelForm):
        author = self.get_object().task.column.project.owner
        if author != self.request.user:
            raise PermissionDenied("You aren't owner of this comment")
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('task_detail',  kwargs={'pk': self.object.task.pk})
#працює неправильно
class DeleteCommentView(LoginRequiredMixin, UserIsAssignedCommentkMixin,DeleteView):
    model = Comment
    template_name = 'tracking/comment_delete.html'

    
    def get_success_url(self):
        return reverse_lazy('task_detail',  kwargs={'pk': self.object.task.pk})

class UpdateTaskView(UserIsAssignedTaskMixin,LoginRequiredMixin,UpdateView):
    model = Task
    template_name = 'tracking/task_update.html'
    fields = ['name','text']
    success_url = reverse_lazy('projects')

    def form_valid(self, form: BaseModelForm):
        author = self.get_object().column.project.owner
        if author != self.request.user:
            raise PermissionDenied("You aren't owner of this project")
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('task_detail',  kwargs={'pk': self.object.pk})
#працює неправильно
class DeleteTaskView(LoginRequiredMixin, UserIsAssignedTaskMixin,DeleteView):
    model = Task
    template_name = 'tracking/task_delete.html' 

    def get_success_url(self):
        return reverse_lazy('project',  kwargs={'pk': self.object.column.project.pk})

class CreateColumnView(CreateView):
    
    form_class = CreateColumnForm
    template_name = 'tracking/create_column.html'

    def form_valid(self, form):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project,id = project_id)
        
        form.instance.project = project
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('project',  kwargs={'pk': self.kwargs['project_id']})
