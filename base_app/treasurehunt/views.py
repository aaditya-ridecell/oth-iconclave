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
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('treasurehunt:question'))
    registered = False

    if request.method == 'POST':
        user_form = forms.UserForm(data=request.POST)
        if user_form.is_valid():
            passmain = user_form.cleaned_data['password']
            passverify = user_form.cleaned_data['confirm_password']
            if passmain == passverify:
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                score = models.Score()
                score.user = user
                score.save()

                registered = True
            else:
                return HttpResponse("Password Don't Match")
        else:
            print(user_form.errors)
    else:
        user_form = forms.UserForm()

    return render(request, 'treasurehunt/signup.html', {
        'user_form': user_form,
        'registered': registered
    })


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('treasurehunt:question'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('treasurehunt:question'))
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


@login_required
def question(request):

    question_fixed = [
        '0', '1', '2', '3', '4', '5wopeiqweoj', '6XYyxasydyaanmp',
        '7dwqeqpdsaaqQ', '8Qweqewqdsapoi', '9dsawqQwqe', '10QASawqeadsp',
        '11IUoiruwefhdsl', '12IYRUEHDSnakhqw', '13KLJcmnxwqeg'
    ]

    current_user = request.user
    sc = models.Score.objects.get(user__exact=current_user)
    ans_fixed = models.AnswerChecker.objects.get(index__exact=sc.score)
    print(ans_fixed)
    print(type(ans_fixed))
    if sc.score == 14:
        return HttpResponse(
            "<h1>Congratulations on Completing The Treasure Hunt</h1>")
    else:
        if request.method == 'POST':
            question_form = forms.Answer(data=request.POST)
            if question_form.is_valid():
                ans = question_form.cleaned_data['answer']
                if ans.lower() == ans_fixed.ans_value():
                    sc.score = sc.score + 1
                    sc.save()
                else:
                    return render(
                        request, 'treasurehunt/question.html', {
                            'question_form': question_form,
                            'score': sc.score,
                            'question_fixed': question_fixed[sc.score],
                        })
            else:
                return render(
                    request, 'treasurehunt/question.html', {
                        'question_form': question_form,
                        'score': sc.score,
                        'question_fixed': question_fixed[sc.score],
                    })
        else:
            question_form = forms.Answer()
        return render(
            request, 'treasurehunt/question.html', {
                'question_form': question_form,
                'score': sc.score,
                'question_fixed': question_fixed[sc.score],
            })


def leaderboard(request):
    leader = models.Score.objects.all().order_by('-score')
    if len(leader) >= 10:
        user_name = []
        for x in leader:
            user_name.append((x.user.username, x.score))
        return render(request, 'treasurehunt/leaderboard.html', {
            'user_name': user_name,
        })
    else:
        user_name = []
        for x in leader:
            user_name.append((x.user.username, x.score))
        return render(request, 'treasurehunt/leaderboard.html', {
            'user_name': user_name,
        })


#t = Score.objects.all().order_by('-score')
# t[0].user.username