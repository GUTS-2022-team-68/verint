from unicodedata import category
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from apps.employees.models import WordOfTheDayWord, Employees, Score, Team
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from utils.scoring import updateTeamScores, getUserScores
import enchant


def index(request):
    return HttpResponse("Hello, world. employees views")

@login_required
def wordoftheday(request):
   

    team_scores = updateTeamScores()

    current_user = Employees.objects.get(user=request.user)

    try:
        words = WordOfTheDayWord.objects.order_by("-height")
        old_word = words[0].word
    except IndexError:
        WordOfTheDayWord.objects.create(word="hello")
        words = WordOfTheDayWord.objects.order_by("-height")
        old_word = words[0].word
    
    d = enchant.Dict("en_UK")
    include_words = []
    exclude_words = []

    context_dict = {"words": words}
    context_dict['teams'] = team_scores
    context_dict['users'] = getUserScores()

    if request.method == "POST":
        
        letters = request.POST.dict()
        
        new_word = ''
        
        for key in letters.keys():
            if 'letter' in key:
                new_word += letters[key]

        if (not d.check(new_word) and new_word not in include_words) or new_word in exclude_words:
            context_dict["error"] = "The word entered is invalid!"
        elif new_word == old_word:
            return HttpResponseRedirect(request.path_info)
        else:
            # Everything went right - Manage score stuff here-----------------------------------
      
            if current_user.score == None:     # Create the user a score record
                score_record = Score.objects.create()
                current_user.score = score_record
                current_user.save()
            else:
                score_record = current_user.score

            score = wordScore(old_word, new_word)   # Calculate the score
            score_record.wotd += score              # Add the score to the database
            score_record.save()

            updateTeamScores()

            print("The user's score is:", Employees.objects.get(user=request.user).score.wotd)

            WordOfTheDayWord.objects.create(word = new_word, height = words[0].height+1)
            return HttpResponseRedirect(request.path_info)

    response = render(request, "games/wotd.html", context = context_dict)
    return response

#Helper Functions
def wordScore(old, new):
    difference_count = 0

    smaller = min([old, new], key=len)
    bigger = max([old, new], key=len)

    for i in range(len(smaller)):
        if smaller[i] != bigger[i]: difference_count += 1
    
    
    score = 6-difference_count-(len(bigger)-len(smaller))
    return score