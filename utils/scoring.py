from apps.employees.models import Team, Employees, Score, Game
from django.db.models import Q
from django.forms.models import model_to_dict

def updateTeamScores():

    # Update the Scores

    teams = Team.objects.all()
    score_dict = {}

    for team in teams:
        score_total = 0

        team_members = Employees.objects.filter(teams=team)

        for member in team_members:
            if member.score != None:
                score_total += member.score.wotd
        
        if team.score == None:
            score_record = Score.objects.create()
            team.score = score_record
            team.save()
        else:
            score_record = team.score
        
        score_record.wotd = score_total
        score_record.save()

        score_dict[team.name] = team.score.wotd

    for team in Team.objects.all():
        print(team.name, ": ", team.score.wotd)

    return dict(sorted(score_dict.items(), key=lambda item: item[1], reverse=True))

def getUserWOTDScores():

    users = Employees.objects.filter(~Q(score=None))
    user_dict = {}

    for user in users:
        user_dict[user.user.username] = user.score.wotd

    return dict(sorted(user_dict.items(), key=lambda item: item[1], reverse=True))

def getTeamScores():

    teams = Team.objects.filter(~Q(score=None))
    team_dict = {}

    for team in teams:
        team_dict[team.name] = model_to_dict(team.score, fields=['wotd'])
    
    return team_dict

def getUserScores():
    users = Employees.objects.filter(~Q(score=None))
    user_dict = {}

    for user in users:
        user_dict[user.user.username] = model_to_dict(user.score, fields=['wotd'])
    
    return user_dict

def getGameStats():
    games = Game.objects.all()
    game_dict = {}

    for game in games:
        game_dict[game.name] = {'plays': game.number_of_plays}

    return game_dict


def getScoreData():

    score_dict = {}

    score_dict['users'] = getUserScores()
    score_dict['teams'] = getTeamScores()
    score_dict['games'] = getGameStats()

    return score_dict


