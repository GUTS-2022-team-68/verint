from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from utils.scoring import getTeamScores
from utils.scoring import getScoreData
from apps.employees.models import Game, Team
from json import dumps


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        messages.success(request, "Registration successful.")
        return render(request, 'index.html')
    else:
        # Return an 'invalid login' error message.
        messages.error(request, "Unsuccessful registration. Invalid information.")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='/accounts/login/')
def leaderboard(request):

    score_data = getScoreData()
    dataJSON = dumps(score_data)

    context_dict = {}
    context_dict['score_data'] = dataJSON

    games = Game.objects.all()
    context_dict['games'] = games

    teams = Team.objects.order_by('-score__total')[:5]

    high_score = 1
    for team in teams:
        if team.score.total > high_score:
            high_score = team.score.total

    team_scores = []

    for team in teams:
        team_scores.append(team.score.total/high_score*100)


    bar_graph_colour_tags = ['bg-danger', 'bg-warning', 'bg-info', 'bg-success', '']
    combined_team_score_data = []
    
    for i in range(len(teams)):
        combined_team_score_data.append([teams[i], team_scores[i], bar_graph_colour_tags[i]])

    context_dict['high_score'] = high_score
    context_dict['teams'] = combined_team_score_data

    # Radio chart

    radio_scores = getTeamScores()

    return render(request, 'leaderboard.html', context_dict)
