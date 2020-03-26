from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game




@login_required()
def home(request):
    return render(request, "castlemaze/home.html", {'app':'castlemaze', 'appname':'Castle Maze'})

@login_required()
def game(request, id):
    game = get_object_or_404(Game, pk=id)
    return render(request, "castlemaze/game.html", {'app':'castlemaze', 'appname':'Castle Maze', 'game': game})

def welcome(request):
    if request.user.is_authenticated:
        return redirect('castlemaze_home')
    else:
        return render(request, 'castlemaze/welcome.html', {'app':'castlemaze', 'appname':'Castle Maze'})
