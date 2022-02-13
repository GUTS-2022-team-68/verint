from unicodedata import category
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from apps.employees.models import WordOfTheDayWord, Employees, Score, Game
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from utils.scoring import updateTeamScores, getUserWOTDScores, getScoreData
from django.forms.models import model_to_dict
import enchant


def index(request):
    return HttpResponse("Hello, world. employees views")


def game_1(request):
    return render(request, 'game1.html')


def game_2(request):
    return render(request, 'game2.html')


def game_4(request):
    return render(request, 'game4.html')

    
@login_required
def wordoftheday(request):
   
    # u = Employees.objects.get(user = request.user)
    
    # #print(model_to_dict(u))

    # print(getScoreData())
    
    # end of tests ----------------------------------------------------------------------
    
    # Update or Create Game Model

    game, created = Game.objects.get_or_create(name = "Word of the Day")
    game.number_of_plays += 1
    game.save()
    
    team_scores = updateTeamScores(game)

    current_user = Employees.objects.get(user=request.user)

    try:
        words = WordOfTheDayWord.objects.order_by("-height")
        old_word = words[0].word
    except IndexError:
        WordOfTheDayWord.objects.create(word="hello")
        words = WordOfTheDayWord.objects.order_by("-height")
        old_word = words[0].word
    
    d = enchant.Dict("en_UK")

    context_dict = {"words": words}
    context_dict['teams'] = team_scores
    context_dict['users'] = getUserWOTDScores()

    if request.method == "POST":
        
        letters = request.POST.dict()
        
        new_word = ''
        
        for key in letters.keys():
            if 'letter' in key:
                new_word += letters[key]

        if not d.check(new_word):
            context_dict["error"] = "This word is not in the dictionary!"
        elif new_word in [word.word for word in words]:
            context_dict["error"] = "This word has already been used!"
        elif new_word == old_word:
            return HttpResponseRedirect(request.path_info)
        else:
            # Everything went right - Manage score stuff here-----------------------------------
      
            if current_user.score == None:     # Create the user a score record
                score_record = Score.objects.create(game = game)
                current_user.score = score_record
                current_user.save()
            else:
                score_record = current_user.score

            score = wordScore(old_word, new_word)   # Calculate the score
            score_record.wotd += score              # Add the score to the database
            score_record.save()

            updateTeamScores(game)

            print("The user's score is:", Employees.objects.get(user=request.user).score.wotd)

            WordOfTheDayWord.objects.create(word = new_word, height = words[0].height+1)
            return HttpResponseRedirect(request.path_info)

    response = render(request, "wordoftheday.html", context = context_dict)
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
