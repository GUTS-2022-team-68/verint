from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


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
    return render(request, 'leaderboard.html')
