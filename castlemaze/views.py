from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game, Cell, Card, Player
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required()
def home(request):
    games_open = Game.objects.filter(status='P').order_by('-id')
    games_started = Game.objects.filter(status='S').order_by('-id')
    return render(request, "castlemaze/home.html", {'app':'castlemaze', 'appname':'Castle Maze', 'games_open':games_open, 'games_started': games_started})

@login_required()
def game(request, id):
    if id == '0':
        game = Game()
        game.save()
        game.new_deck()
        game.generate_cell_list()
        game.save()
        return redirect('castlemaze_game', id=game.pk)
    else :
        game = get_object_or_404(Game, pk=id)
        if game.player_set.filter(user=request.user):
            board = game.get_board_for_player(request.user)
        else:
            board = game.get_board_for_spectator()
        return render(request, "castlemaze/game.html", {'app':'castlemaze', 'appname':'Castle Maze', 'game': game, 'board': board})

def welcome(request):
    if request.user.is_authenticated:
        return redirect('castlemaze_home')
    else:
        return render(request, 'castlemaze/welcome.html', {'app':'castlemaze', 'appname':'Castle Maze'})


@login_required()
def action_request(request):
    if request.method == 'POST':
        cell = get_object_or_404(Cell, pk = request.POST.get('cell_id'))
        game = cell.game
        if cell.cell_type == 'red_team' or cell.cell_type == 'blue_team':
            game.add_player_to_team(request.user, cell.cell_type)
            game.send_board_to_all()
        if cell.cell_type == 'game_status':
            game.start_game()
            game.send_board_to_all()
        if cell.cell_type == 'player_tile_hand':
            card = Player.objects.get(game=game, user=request.user).tile_cards.all()[cell.x]
            game.card_selected = card
            game.save()
            game.send_board_to_user(request.user)
        if cell.cell_type == 'player_action_hand':
            card = Player.objects.get(game=game, user=request.user).action_cards.all()[cell.x]
            game.card_selected = card
            game.save()
            game.send_board_to_user(request.user)
        if cell.cell_type == 'maze':
            game.action(cell,request.user)
            game.set_next_player()
            game.send_board_to_all()
        return HttpResponse("Ok")