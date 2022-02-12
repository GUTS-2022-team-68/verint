from unicodedata import category
from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from apps.employees.models import WordOfTheDayWord
from django.shortcuts import redirect


def index(request):
    return HttpResponse("Hello, world. employees views")

def wordoftheday(request):

    words = WordOfTheDayWord.objects.order_by("-height")

    context_dict = {"words": words}

    if request.method == "POST":
        
        letters = request.POST.dict()
        
        new_word = ''
        
        for key in letters.keys():
            if 'letter' in key:
                new_word += letters[key]

        
        WordOfTheDayWord.objects.create(word = new_word, height = words[0].height+1)
        return HttpResponseRedirect(request.path_info)

    response = render(request, "games/wotd.html", context = context_dict)
    return response
