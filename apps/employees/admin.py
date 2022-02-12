from django.contrib import admin
from apps.employees.models import WordOfTheDayWord, Score, Employees, Team

admin.site.register(WordOfTheDayWord)
admin.site.register(Score)
admin.site.register(Team)
admin.site.register(Employees)