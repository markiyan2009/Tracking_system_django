from django.urls import path
from tracking import views

urlpatterns = [
    path("projects", views.ProjectsListview.as_view(), name="projects"),
    path("<int:pk>",views.ProjectDetailView.as_view(), name = "project"),
    path("login/", views.login_view, name="login"),
    path('add_project', views.CreateProjectView.as_view(),name='add_project'), 
]