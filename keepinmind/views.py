from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def welcome(request):
    if request.user.is_authenticated:
        return redirect('keepinmind_home')
    else:
        return render(request, 'keepinmind/welcome.html', {'app':'keepinmind', 'appname':'Keep in mind !'})

@login_required()
def home(request):
    return render(request,'keepinmind/home.html', {'app':'keepinmind', 'appname':'Keep in mind !'})
