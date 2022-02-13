from django.contrib import admin
from apps.employees.models import WordOfTheDayWord, Score, Employees, Team, Game

admin.site.register(WordOfTheDayWord)
admin.site.register(Score)
admin.site.register(Team)
admin.site.register(Employees)
admin.site.register(Game)