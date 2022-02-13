from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=50, unique=True)
    number_of_plays = models.IntegerField(default=0)

class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    wotd = models.IntegerField(default=0)
    tictactoe = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.total = self.wotd+self.tictactoe
        super().save(*args, **kwargs)

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
