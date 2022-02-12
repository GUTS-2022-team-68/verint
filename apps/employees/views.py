from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. employees views")


def game_1(request):
    return render(request, 'game1.html')


def game_2(request):
    return render(request, 'game2.html')


def game_3(request):
    return render(request, 'game3.html')


def game_4(request):
    return render(request, 'game4.html')
