from django.shortcuts import render
from . import forms
# Create your views here.
from treasurehunt import models
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'treasurehunt/index.html')


def register(request):

    registered = False

    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            score = models.Score()
            score.user = user
            score.save()

            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = forms.UserForm()

    return render(request, 'treasurehunt/registration.html', {
        'user_form': user_form,
        'registered': registered
    })


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('treasurehunt:index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed")
            print("UserName : {} and password {} ".format(username, password))
            return HttpResponse("Invalid Login Details")
    else:
        return render(request, 'treasurehunt/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('treasurehunt:index'))


# @login_required
# def question(request):
