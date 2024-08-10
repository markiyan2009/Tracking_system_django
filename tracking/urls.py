from django.urls import path
from tracking import views

urlpatterns = [
    path("projects", views.ProjectsListview.as_view(), name="projects"),
]