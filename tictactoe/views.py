from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Game, Invitation
from django.contrib.auth.decorators import login_required
from .forms import InvitationForm, MoveForm
from django.views.generic import ListView, CreateView


@login_required()
def home(request):
    my_games = Game.objects.games_for_user(request.user)
    active_games = my_games.active()
    finished_games = my_games.difference(active_games)
    invitations = request.user.invitations_received.all()
    return render(request, "tictactoe/home.html", {'active_games': active_games, 'finished_games':finished_games,'invitations':invitations, 'app':'tictactoe', 'appname':'Morpion'})

def welcome(request):
    if request.user.is_authenticated:
        return redirect('tictactoe_home')
    else:
        return render(request, 'tictactoe/welcome.html', {'app':'tictactoe', 'appname':'Morpion'})

@login_required()
def new_invitation(request):
    if request.method == "POST":
        invitation = Invitation(from_user=request.user)
        form = InvitationForm(request.user, instance=invitation, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('tictactoe_home')
    else:
        form = InvitationForm(request.user)
    return render(request, "tictactoe/new_invitation_form.html", {'form':form})

@login_required()
def accept_invitation(request, id):
    invitation = get_object_or_404(Invitation, pk=id)
    if not request.user == invitation.to_user:
        raise PermissionDenied
    if request.method == 'POST':
        if "accept" in request.POST:
            game = Game.objects.create(first_player=invitation.to_user, second_player=invitation.from_user)
            invitation.delete()
            return redirect(game)
        invitation.delete()
        return redirect('tictactoe_home')
    else :
        return render(request, "tictactoe/accept_invitation_form.html", {'invitation': invitation})


@login_required()
def game_detail(request, id):
    game = get_object_or_404(Game, pk=id)
    context = {'game': game}
    if game.is_users_move(request.user):
        context['form'] = MoveForm()
    return render(request, "tictactoe/game_details.html", context)

@login_required()
def make_move(request, id):
    game = get_object_or_404(Game, pk=id)
    if not game.is_users_move(request.user):
        raise PermissionDenied
    move = game.new_move()
    form = MoveForm(instance=move, data=request.POST)
    if form.is_valid():
        move.save()
        return redirect('tictactoe_detail', id)
    else:
        return render(request, 'tictactoe/game_details.html', {'game':game, 'form':form})

class AllGamesList(ListView):
    model = Game