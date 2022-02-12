from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=64)
    t_id = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Employees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    e_id = models.CharField(max_length=64)
    current_role = models.CharField(max_length=64)  # "coder"
    teams = models.ManyToManyField(Team, related_name="employees", blank=True)
    hire_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.first_name
