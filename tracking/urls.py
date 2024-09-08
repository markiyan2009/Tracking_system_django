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
    path('<int:column_id>', views.CreateTaskView.as_view(), name='add_task'),
    path('comment_update/<int:pk>', views.UpdateCommentView.as_view(), name = 'update_comment'),
    path("comment_delete/<int:pk>", views.DeleteCommentView.as_view(),name='delete_comment'),
    path('task_update/<int:pk>', views.UpdateTaskView.as_view(), name='task_update'),
    path('task_delete/<int:pk>', views.DeleteTaskView.as_view(), name='task_delete')
]