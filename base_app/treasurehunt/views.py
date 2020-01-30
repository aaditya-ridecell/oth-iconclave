from django.shortcuts import render
from . import forms
# Create your views here.
from treasurehunt import models
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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
