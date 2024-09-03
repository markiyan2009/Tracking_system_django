from django.contrib import admin
from tracking.models import Project, Column, Task,Comment
# Register your models here.
admin.site.register(Project)
admin.site.register(Column)
admin.site.register(Task)
admin.site.register(Comment)