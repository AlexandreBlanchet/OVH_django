from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game, Cell, Card, Player
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse





@login_required()
def home(request):
    games = Game.objects.all()
    return render(request, "castlemaze/home.html", {'app':'castlemaze', 'appname':'Castle Maze', 'games_list':games})

@login_required()
def game(request, id):
    if id == '0':
        game = Game()
        game.save()
        game.new_deck()

        player = Player(user=User.objects.get(username='alice'))
        player.save()
        player2 = Player(user=User.objects.get(username='ablanche'))
        player2.save()
        game.players.add(player, player2)
        game.generate_cell_list()

        game.save()
        return redirect('castlemaze_game', id=game.pk)
    else :
        game = get_object_or_404(Game, pk=id)
        if not game.players.filter(user = request.user) :
            return redirect('castlemaze_home')
        board = game.get_board(request.user)

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
        if cell.cell_type == 'player_hand' and not cell.game.card_selected:
            card = cell.game.players.get(user=request.user).cards.all()[cell.x]
            cell.game.card_selected = card
            cell.game.save()
        if cell.cell_type == 'maze' and cell.game.card_selected:
            cell.game.move_cards(cell,request.user)
        board = cell.game.get_board(request.user)
        # return render(request, 'castlemaze/welcome.html', {'app':'castlemaze', 'appname':'Castle Maze', 'content': content})
        return JsonResponse(board, safe=False)

@login_required()
def start_game(request):
    if request.method == 'POST':
        game = Game.objects.get(pk=request.POST.get('game_id'))
        game.start_game()
        board = game.get_board(request.user)
        # return render(request, 'castlemaze/welcome.html', {'app':'castlemaze', 'appname':'Castle Maze', 'content': content})
        return JsonResponse(board, safe=False)
