from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Game, Cell, Card, Player
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
        game.generate_cell_list()

        player = Player.objects.get(pk=1)
        game.players.add(player)
        game.draw_cards_to_players()

        game.save()
        # TODO correct issue with redirect
        return redirect('castlemaze_game', id=game.pk)
    else :
        game = get_object_or_404(Game, pk=id)
        player = get_object_or_404(Player, user = request.user)
        if not game.players.filter(user = request.user) :
            return redirect('castlemaze_home')

        cards = game.get_player_cards(request.user) 
    
    return render(request, "castlemaze/game.html", {'app':'castlemaze', 'appname':'Castle Maze', 'game': game, 'cards':cards})

def welcome(request):
    if request.user.is_authenticated:
        return redirect('castlemaze_home')
    else:
        return render(request, 'castlemaze/welcome.html', {'app':'castlemaze', 'appname':'Castle Maze'})

@login_required()
def action_request(request):
    if request.method == 'POST':
        cell = get_object_or_404(Cell, pk = request.POST.get('cell_id'))
        # TODO check if it's the correct user who has the card
        card = get_object_or_404(Card, pk = request.POST.get('card_id'))
        cell.card = card
        cell.save()
        game = Game.objects.get(pk=cell.game.pk)
        cell_list = game.move_cells(cell)

        player = get_object_or_404(Player, user=request.user)
        player.cards.remove(card)
        player.cards.add(game.deck.draw())
        player.save()

        # return render(request, 'castlemaze/welcome.html', {'app':'castlemaze', 'appname':'Castle Maze', 'content': content})
        return JsonResponse(cell_list, safe=False)
