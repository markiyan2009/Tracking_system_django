from django.urls import path
from tracking import views

urlpatterns = [
    path("projects", views.ProjectsListview.as_view(), name="projects"),
    path("projects/<int:pk>",views.ProjectDetailView.as_view(), name = "project"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path('add_project', views.CreateProjectView.as_view(),name='add_project'), 
    path('tasks/<int:pk>', views.TaskDetailView.as_view(), name='task_detail'),
    path('logout', views.CustomLogoutView.as_view(), name = 'logout'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('task/<int:pk>/complete', views.TaskCompleteView.as_view(), name='complete_task'),
    path('<str:name>', views.CreateTaskView.as_view(), name='add_task'),
]