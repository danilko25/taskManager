from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Task(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField
    deadline = models.DateTimeField
    priority = models.IntegerField
    status = models.CharField
    creation_date = models.DateTimeField

    def __str__(self):
        return f"Task: {self.title},  status: {self.status},  deadline: {self.deadline}"
