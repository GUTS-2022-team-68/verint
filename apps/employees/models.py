from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.forms import IntegerField


class Score(models.Model):
    wotd = models.IntegerField(default=0)
    remaining_letters = IntegerField(default=5)

class Team(models.Model):
    name = models.CharField(max_length=64)
    t_id = models.CharField(max_length=64)
    score = models.OneToOneField(Score, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Employees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    e_id = models.CharField(max_length=64)
    current_role = models.CharField(max_length=64)  # "coder"
    teams = models.ManyToManyField(Team, related_name="employees", blank=True)
    hire_date = models.DateTimeField(null=True, blank=True)
    score = models.OneToOneField(Score, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

class WordOfTheDayWord(models.Model):
    word = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    height = models.IntegerField(default=0)
