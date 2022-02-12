from apps.employees.models import Team, Employees, Score
from django.db.models import Q

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

def getUserScores():

    users = Employees.objects.filter(~Q(score=None))
    user_dict = {}

    for user in users:
        user_dict[user.user.username] = user.score.wotd

    return dict(sorted(user_dict.items(), key=lambda item: item[1], reverse=True))
