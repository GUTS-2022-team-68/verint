from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import NewUserForm


def register_view(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        messages.success(request, "Registration successful.")
        return redirect("/")
    else:
        # Return an 'invalid login' error message.
        messages.error(request, "Invalid Login")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='/accounts/login/')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='/accounts/login/')
def leaderboard(request):
    return render(request, 'leaderboard.html')
