import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GUTS_team68.settings")

import django
django.setup()
from apps.employees.models import Team, Game, Score, Employees
from django.contrib.auth.models import User

def populate():

    p = Game.objects.get_or_create(name = "Word of the Day")[0]
    p.save()
    p = Game.objects.get_or_create(name = "Tic Tac Toe")[0]
    p.save()
    p = Game.objects.get_or_create(name = "Truths and Lies")[0]
    p.save()
    p = Game.objects.get_or_create(name = "Game 4")[0]
    p.save()

    a = Team.objects.get_or_create(name = "Admin", id="0")[0]
    a.score = Score.objects.create()
    a.save()
    d = Team.objects.get_or_create(name = "Development", id="1")[0]
    d.score = Score.objects.create()
    d.save()
    m = Team.objects.get_or_create(name = "Marketing", id="2")[0]
    m.score = Score.objects.create()
    m.save()
    h = Team.objects.get_or_create(name = "HR", id="3")[0]
    h.score = Score.objects.create()
    h.save()
    r = Team.objects.get_or_create(name = "Research", id="4")[0]
    r.score = Score.objects.create()
    r.save()
    
    u = User.objects.get_or_create(username = "Jake", password="hello", id="0")[0]
    p = Employees.objects.get_or_create(user = u)[0]
    p.score = Score.objects.create()
    p.teams.set(d)
    p.save()

    p = Employees.objects.get_or_create()[0]
    p.score = Score.objects.create()
    p.teams.set(d)
    p.user = User.objects.get_or_create(username = "Helena", password="hello", id="1")[0]
    p.save()

    p = Employees.objects.get_or_create()[0]
    p.score = Score.objects.create()
    p.teams.set(d)
    p.user = User.objects.get_or_create(username = "Alfie", password="hello", id="2")[0]
    p.save()

    p = Employees.objects.get_or_create()[0]
    p.score = Score.objects.create()
    p.teams.set(d)
    p.user = User.objects.get_or_create(username = "Alice", password="hello", id="3")[0]
    p.save()

populate()


