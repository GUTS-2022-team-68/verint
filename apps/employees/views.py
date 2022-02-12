import enum
import re
from unicodedata import category
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from apps.employees.models import WordOfTheDayWord
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import enchant


def index(request):
    return HttpResponse("Hello, world. employees views")

@login_required
def wordoftheday(request):

    #random scores - update when database allows it
    scores = [["Development", 100],
            ["Human Resources", -5],
            ["Management", 45],
            ["Marketing", 12],
            ["Analytics", 73]]

    scores.sort(key=lambda x: x[1], reverse=True)

    words = WordOfTheDayWord.objects.order_by("-height")
    old_word = words[0].word

    d = enchant.Dict("en_UK")
    include_words = []
    exclude_words = []

    context_dict = {"words": words}
    context_dict['scores'] = scores

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

            score = wordScore(old_word, new_word)
            print(score)

            WordOfTheDayWord.objects.create(word = new_word, height = words[0].height+1)
            return HttpResponseRedirect(request.path_info)

    response = render(request, "games/wotd.html", context = context_dict)
    return response

#Helper Functions
def wordScore(old, new):
    difference_count = 0

    if len(old) < len(new):
        for i, letter in enumerate(new):
            if letter != old[i]:
                difference_count += 1
    else:
        for i, letter in enumerate(old):
            if letter != new[i]:
                difference_count += 1
    
    score = 6-difference_count
    return score