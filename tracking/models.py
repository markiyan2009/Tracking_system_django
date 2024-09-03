from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.name


class Column(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ("todo","To do"),
        ('inprogres', "In progres"),
        ("done","Done"),
    ]
    name = models.CharField(max_length=150)
    text = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="todo")
    column = models.ForeignKey(Column,on_delete=models.CASCADE, related_name="tasks")

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    owner = models.ForeignKey(User, models.CASCADE)
    task = models.ForeignKey(Task, models.CASCADE, null=True)
    text = models.TextField()
    post_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.author.username

