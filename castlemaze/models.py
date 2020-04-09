from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
import random
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging

GAME_STATUS_CHOICES = (
    ('P', 'Preparation'),
    ('S', 'Started'),
    ('B','Blue win'),
    ('R', 'Red win'),
)

CELL_TYPES = {
    'maze' : {'offset_top': 20, 'offset_left': 20, 'width': 60, 'height': 60, 'class': 'castlemaze-maze' },
    'player_tile_hand' : {'offset_top': 330, 'offset_left': 890, 'width': 110, 'height': 150, 'class': 'castlemaze-card' },
    'player_action_hand' : {'offset_top': 490, 'offset_left': 890, 'width': 110, 'height': 150, 'class': 'castlemaze-card' },
    'red_team' : {'offset_top': 10, 'offset_left': 1000, 'width': 250, 'height': 350, 'class': 'castlemaze-team-red' },
    'blue_team' : {'offset_top': 10, 'offset_left': 1260, 'width': 250, 'height': 350, 'class': 'castlemaze-team-blue' },
    'deck' : {'offset_top': 160, 'offset_left': 870, 'width': 100, 'height': 150, 'class': 'castlemaze-card' },
    'game_status' : {'offset_top': 230, 'offset_left': 1000, 'width': 300, 'height': 150, 'class': 'castlemaze-game-status' },
    'pass_button' : {'offset_top': 570, 'offset_left': 690, 'width': 300, 'height': 150, 'class': 'castlemaze-game-pass-button' },

}

BOARD_WIDTH=14
BOARD_HEIGTH=9
NUMBER_OF_CARDS_PER_PLAYER=10

NOT_CLICKABLE_COORD = (
    (0,0),
    (0,BOARD_HEIGTH-1),
    (BOARD_WIDTH-1,0),
    (BOARD_WIDTH-1,BOARD_HEIGTH-1),
    (0,4),
    (BOARD_WIDTH-1,4),
    (3,0),
    (3,BOARD_HEIGTH-1),
    (10,0),
    (10,BOARD_HEIGTH-1),
)

CASTLE_COORD = (
    (3,4),
    (10,4),
)

logger = logging.getLogger(__name__)

# players can be 'all', 'others', 'player'
def send_update_to_players(game_id, players, user, json):
    channel_layer = get_channel_layer()
    if players == 'all':
        username = ''
    else:
        username = user.username
    async_to_sync(channel_layer.group_send)(
        'game_' + str(game_id),
        { 'type': 'chat_message','message': { 'players': players, 'username': username, 'update': json}}
    )

class Card(models.Model):
    img = models.CharField(max_length=30, default="cell.png")
    card_type = models.CharField(max_length=100, default='tile')
    trap = models.CharField(max_length=100, default='')

    open_top = models.BooleanField(default=False)
    open_left = models.BooleanField(default=False)
    open_bottom = models.BooleanField(default=False)
    open_right = models.BooleanField(default=False)
    number_of_moves = models.IntegerField(default=0)

    activated_open_top = models.BooleanField(default=False)
    activated_open_left = models.BooleanField(default=False)
    activated_open_bottom = models.BooleanField(default=False)
    activated_open_right = models.BooleanField(default=False)

    def get_tile_display(self):
        return 'img/' + self.img + '.png'
    
    def get_card_display(self):
        if self.trap :
            return 'img/card_'  + self.trap + '_'  + self.img + '.png'
        else:
            return 'img/card_' + self.img + '.png'

    def get_trap_display(self):
        return 'img/trap_' + self.trap + '_' + self.img + '.png'
    
    def get_trap_activated_display(self):
        return 'img/trap_activated_' + self.trap + '_' + self.img + '.png'

    def get_tile_style(self):
        return 'width:60px'
    
    def get_card_style(self):
        return 'width:100px'
    

class Deck(models.Model):
    card_order = models.CharField(max_length=3000, null=True)
    deck_type = models.CharField(max_length=100, default='tile')
    game = models.ForeignKey('Game', on_delete=models.CASCADE, null=True)

    def add_card(self, card):
        self.card_order += ';' + str(card.pk)

    def draw(self):
        card = None
        if len(self.card_order) > 0:
            card = Card.objects.get(pk=int(self.card_order.split(';')[0]))
            self.card_order = ';'.join(self.card_order.split(';')[1:])
            self.save()
        return card

class Player(models.Model):
    player_id = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tile_cards = models.ManyToManyField(Card, related_name='tile_cards')
    action_cards = models.ManyToManyField(Card, related_name='action_cards')
    pawn_cell = models.ForeignKey('Cell', on_delete=models.CASCADE, null = True)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, null = True)
    team = models.CharField(max_length=50)
    status_played_tile = models.BooleanField(default=False)
    status_played_action = models.BooleanField(default=False)
    remaining_moves = models.IntegerField(default=0)
    trap_visible = models.ManyToManyField(Card, related_name='trap_cards')

class Game(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='P', choices=GAME_STATUS_CHOICES)
    card_selected = models.ForeignKey(Card, on_delete=models.CASCADE, null=True)
    max_number_of_players = models.IntegerField(default=6)
    player_turn = models.IntegerField(default=0)
    team_turn = models.CharField(max_length=100, default='red_team')
    last_cell_played = models.ForeignKey('Cell', related_name='last_cell_player', on_delete=models.CASCADE, null = True)
    activated_traps = models.ManyToManyField(Card, related_name='activated_traps')


    def get_playing_player(self):
        team_players = self.player_set.filter(team=self.team_turn)
        player_id = self.player_turn % team_players.count()
        return self.player_set.get(player_id=player_id, team=self.team_turn)

    def force_next_player(self):
        if self.team_turn == 'blue_team':
            self.player_turn = (self.player_turn + 1) % 4
            self.team_turn = 'red_team'
        else :
            self.team_turn = 'blue_team'
        self.save()
        
        player = self.get_playing_player()
        player.status_played_tile = False
        player.status_played_action = False
        player.save()


    def set_next_player(self):
        player = self.get_playing_player()
        if player.status_played_tile and player.status_played_action and player.remaining_moves <= 0:
            self.force_next_player()

    def add_player_to_team(self, user, team):

        if not self.player_set.filter(user=user):
            player = Player(user=user)
        else :
            player = self.player_set.filter(user=user)[0]
            if player.team == team:
                send_update_to_players(self.pk, 'all', '', {'game_status': [{'elem_id': player.pk, 'elem_text': '', 'left': 0, 'top': 0, 'class': ''}]})
                
                player.delete()

                return
        i = 0
        while i < 4 and self.player_set.filter(team=team, player_id=i):
            i += 1
        player.player_id = i
        player.game = self
        player.team = team
        player.save()
        
        
    def board(self):
        return self.cell_set.all()

    def send_board_to_all(self):
        # send maze to non player 
        send_update_to_players(self.pk, 'all', '', self.get_board_for_spectator())
        for player in self.player_set.all():
            send_update_to_players(self.pk, 'user', player.user, self.get_board_for_player(player.user))
    
    def send_board_to_user(self, user):
        send_update_to_players(self.pk, 'user', user, self.get_board_for_player(user))


    def get_board_for_spectator(self):
        """Return the board"""
        board = {}
        board['cells'] = self.get_cells()
        board['cards'] = self.get_maze_cards_positions() + self.get_deck_cards() 
        board['pawns'] = self.get_players_pawn_positions()
        board['game_status'] = self.get_players()+ self.get_game_status()
        return board

    def get_board_for_player(self, user):
        """Return the board"""
        board = {}
        board['cells'] = self.get_cells_for_player(user)
        board['cards'] = self.get_maze_cards_positions(user) + self.get_deck_cards() + self.get_other_players_cards(user) + self.get_player_cards(user)
        board['pawns'] = self.get_players_pawn_positions()
        board['game_status'] = self.get_players() + self.get_game_status(user)
        return board

    def get_game_status(self, user = ''):
        list_status = []
        cell_red_team = self.cell_set.get(cell_type='red_team')
        cell_blue_team = self.cell_set.get(cell_type='blue_team')
        cell_status = self.cell_set.get(cell_type='game_status')
        if self.status == 'P':
            if user != '':
                player = self.player_set.filter(user=user)
            else:
                player = ''

          
            text_blue = 'Join blue team'
            text_red = 'Join red team'
            if player and  player[0].team == 'red_team':
                text_red = 'Leave'
            if player and  player[0].team == 'blue_team':
                text_blue = 'Leave'
            if self.player_set.filter(team='red_team').count() == 4 and ((player and  player[0].team != 'red_team') or not player):
                text_red = 'Team full'
            if self.player_set.filter(team='blue_team').count() == 4 and ((player and  player[0].team != 'blue_team') or not player):
                text_blue = 'Team full'
            list_status.append({'elem_id': 100, 'elem_text': text_red, 'left': cell_red_team.get_left_offset()-30, 'top': cell_red_team.get_top_offset()+150, 'display': '', 'class': 'castlemaze-text'})
            list_status.append({'elem_id': 102, 'elem_text': text_blue, 'left': cell_blue_team.get_left_offset()-30, 'top': cell_blue_team.get_top_offset()+150, 'display': '', 'class': 'castlemaze-text'})
            if player and player[0] == self.player_set.all()[0]:
                list_status.append({'elem_id': 104, 'elem_text': 'Start the game', 'left': cell_status.get_left_offset()+80, 'top': cell_status.get_top_offset()+20, 'display': '', 'class': 'castlemaze-text'})
        if self.status == 'S':
            list_status.append({'elem_id': 100, 'elem_text': '', 'left': cell_red_team.get_left_offset(), 'top': cell_red_team.get_top_offset()+150, 'display': '', 'class': 'castlemaze-text'})
            list_status.append({'elem_id': 102, 'elem_text': '', 'left': cell_blue_team.get_left_offset(), 'top': cell_blue_team.get_top_offset()+150, 'display': '', 'class': 'castlemaze-text'})
            list_status.append({'elem_id': 104, 'elem_text': "It's " + self.get_playing_player().user.username + ' turn !', 'left': cell_status.get_left_offset()+80, 'top': cell_status.get_top_offset()+20, 'display': '', 'class': 'castlemaze-text'})
            cell_pass = self.cell_set.get(cell_type='pass_button')
            list_status.append({'elem_id': 106, 'elem_text': 'Pass', 'left': cell_pass.get_left_offset(), 'top': cell_pass.get_top_offset()+20, 'display': '', 'class': 'castlemaze-text'})

        if self.status == 'B':
            list_status.append({'elem_id': 104, 'elem_text': 'Blue team won !', 'left': cell_status.get_left_offset()+80, 'top': cell_status.get_top_offset()+20, 'display': '', 'class': 'castlemaze-text'})
        if self.status == 'R':
            list_status.append({'elem_id': 104, 'elem_text': 'Red team won !', 'left': cell_status.get_left_offset()+80, 'top': cell_status.get_top_offset()+20, 'display': '', 'class': 'castlemaze-text'})
        
        
        return list_status

    def get_players(self):
        list_players = []
        cell_red_team = self.cell_set.get(cell_type='red_team')
        cell_blue_team = self.cell_set.get(cell_type='blue_team')
        for player in self.player_set.all():
            if player.team == 'red_team':
                list_players.append({'elem_id': player.pk, 'elem_text':player.user.username, 'left': cell_red_team.get_left_offset(), 'top': cell_red_team.get_top_offset()+30*player.player_id, 'display': f'img/player_{player.team}_{player.player_id+1}.png', 'class': 'castlemaze-text'})
            else:
                list_players.append({'elem_id': player.pk, 'elem_text':player.user.username, 'left': cell_blue_team.get_left_offset(), 'top': cell_blue_team.get_top_offset()+30*player.player_id, 'display': f'img/player_{player.team}_{player.player_id+1}.png', 'class': 'castlemaze-text'})
        return list_players


    def get_card_open_status(self, card, direction):
        activated = card in self.activated_traps.all()
        if direction == 'top':
            if activated:
                return card.activated_open_top
            else:
                return card.open_top
        if direction == 'left':
            if activated:
                return card.activated_open_left
            else:
                return card.open_left
        if direction == 'bottom':
            if activated:
                return card.activated_open_bottom
            else:
                return card.open_bottom
        if direction == 'right':
            if activated:
                return card.activated_open_right
            else:
                return card.open_right




    def get_available_neighbours(self, maze, cell_elem, depth, seen):
        if depth == 0 :
            return [cell_elem]
        neighbours = [cell_elem]
        seen.append(cell_elem)
        card = cell_elem.card
        if self.get_card_open_status(card, 'top') and maze[cell_elem.y-1][cell_elem.x] and maze[cell_elem.y-1][cell_elem.x] not in seen and maze[cell_elem.y-1][cell_elem.x].card and self.get_card_open_status(maze[cell_elem.y-1][cell_elem.x].card, 'bottom'):
            neighbours += self.get_available_neighbours(maze, maze[cell_elem.y-1][cell_elem.x], depth - 1, seen)
        if self.get_card_open_status(card, 'right') and maze[cell_elem.y][cell_elem.x+1] and maze[cell_elem.y][cell_elem.x+1] not in seen and maze[cell_elem.y][cell_elem.x+1].card and self.get_card_open_status(maze[cell_elem.y][cell_elem.x+1].card, 'left'):
            neighbours += self.get_available_neighbours(maze, maze[cell_elem.y][cell_elem.x+1], depth - 1, seen)
        if self.get_card_open_status(card, 'bottom') and maze[cell_elem.y+1][cell_elem.x] and maze[cell_elem.y+1][cell_elem.x] not in seen and maze[cell_elem.y+1][cell_elem.x].card and self.get_card_open_status(maze[cell_elem.y+1][cell_elem.x].card, 'top'):
            neighbours += self.get_available_neighbours(maze, maze[cell_elem.y+1][cell_elem.x], depth - 1, seen)
        if self.get_card_open_status(card, 'left') and maze[cell_elem.y][cell_elem.x-1] and maze[cell_elem.y][cell_elem.x-1] not in seen and maze[cell_elem.y][cell_elem.x-1].card and self.get_card_open_status(maze[cell_elem.y][cell_elem.x-1].card, 'right'):
            neighbours += self.get_available_neighbours(maze, maze[cell_elem.y][cell_elem.x-1], depth - 1, seen)            
        return neighbours
        

    def get_cells_for_action(self, player_cell):
        maze = [[None for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGTH)]
        players_cell = [player.pawn_cell for player in self.player_set.all()]
        players_cell.remove(player_cell)
        for cell in self.cell_set.filter(cell_type='maze'):
            if cell not in players_cell:
                maze[cell.y][cell.x] = cell
        return self.get_available_neighbours(maze, player_cell, 1, [])


    def get_cells(self):
        cells = []
        for cell in self.cell_set.all() :
            if ((cell.cell_type == 'red_team' and self.player_set.filter(team='red_team').count() < 4) or (cell.cell_type == 'blue_team'and self.player_set.filter(team='blue_team').count() < 4)) and self.status == 'P':
                cells.append({'cell_id':cell.pk, 'clickable': True, 'class' : cell.get_class() + ' clickable', 'left': cell.get_left_offset(), 'top': cell.get_top_offset()})
            else :
                cells.append({'cell_id':cell.pk, 'clickable': False, 'class' : cell.get_class(), 'left': cell.get_left_offset(), 'top': cell.get_top_offset()})
        return cells

    def get_cells_for_player(self, user):
        # TODO getting only modified cards
        cells = []
        if self.card_selected and not self.card_selected.card_type == 'tile' :
             available_cells = self.get_cells_for_action(self.player_set.get(user=user).pawn_cell)

        # Cells to avoid because of players on the other side and if the last play is a border cell we can't move the lane in the other way
        border_cells_to_avoid = []
        for player in self.player_set.all():
            if player.pawn_cell and player.pawn_cell.x == 1:
                border_cells_to_avoid.append((BOARD_WIDTH - 1,player.pawn_cell.y))
            if player.pawn_cell and player.pawn_cell.x == BOARD_WIDTH - 2:
                border_cells_to_avoid.append((0,player.pawn_cell.y))
            if player.pawn_cell and player.pawn_cell.y == 1:
                border_cells_to_avoid.append((player.pawn_cell.x,BOARD_HEIGTH-1))
            if player.pawn_cell and player.pawn_cell.y == BOARD_HEIGTH-2:
                border_cells_to_avoid.append((player.pawn_cell.x,0))

        if self.last_cell_played and self.last_cell_played.x == 0:
            border_cells_to_avoid.append((BOARD_WIDTH - 1,self.last_cell_played.y))
        if self.last_cell_played and self.last_cell_played.x == BOARD_WIDTH - 1:
            border_cells_to_avoid.append((0,self.last_cell_played.y))
        if self.last_cell_played and self.last_cell_played.y == 0:
            border_cells_to_avoid.append((self.last_cell_played.x,BOARD_HEIGTH-1))
        if self.last_cell_played and self.last_cell_played.y == BOARD_HEIGTH-1:
            border_cells_to_avoid.append((self.last_cell_played.x,0))        

        for cell in self.cell_set.all() :
            clickable = False
            click_class = ''
            player = self.get_playing_player()
            if player.user == user and self.status == 'S':
                if cell.cell_type == 'pass_button':
                    clickable = True
                    click_class = ' clickable'

                if cell.cell_type == 'player_tile_hand' and player.status_played_tile == False :
                    clickable = True
                    click_class = ' clickable'
                    if self.card_selected == player.tile_cards.all()[cell.x]:
                        click_class = ' selected'
                if cell.cell_type == 'player_action_hand' and player.status_played_action == False :
                    clickable = True
                    click_class = ' clickable'
                if cell.cell_type == 'player_action_hand'  and self.card_selected == player.action_cards.all()[cell.x]:
                    click_class = ' selected'

                if (cell.x, cell.y) not in border_cells_to_avoid and self.card_selected and self.card_selected.card_type == 'tile'and cell.cell_type == 'maze' and (cell.x == 0 or cell.x == BOARD_WIDTH - 1 or cell.y == 0 or cell.y == BOARD_HEIGTH - 1):
                    clickable = True
                    click_class = ' clickable'
                if self.card_selected and not self.card_selected.card_type == 'tile' and cell in available_cells:
                    clickable = True
                    click_class = ' clickable'

                if (cell.x, cell.y) in NOT_CLICKABLE_COORD and cell.cell_type == 'maze' :
                    clickable = False
                    click_class = ''



            if self.status == 'P' and ((cell.cell_type == 'game_status' and self.player_set.all()[0].user == user) or cell.cell_type == 'blue_team' or cell.cell_type == 'red_team'):
                clickable = True
                click_class = ' clickable'
            if self.status == 'P' and cell.cell_type == 'blue_team' and self.player_set.filter(user=user)[0].team != 'blue_team' and self.player_set.filter(team='blue_team').count() == 4:
                clickable = False
                click_class = ''
            if self.status == 'P' and cell.cell_type == 'red_team' and self.player_set.filter(user=user)[0].team != 'red_team' and self.player_set.filter(team='red_team').count() == 4:
                clickable = False
                click_class = ''

            cells.append({'cell_id': cell.pk, 'clickable': clickable, 'class' : cell.get_class() + click_class, 'left': cell.get_left_offset(), 'top': cell.get_top_offset()})
        return cells

    def get_maze_cards_positions(self, user=None):
        # TODO change class name using dict
        list_cards = []
        if user :
            player = self.player_set.get(user=user)
        for cell in self.cell_set.all():
            if cell.card :
                display = cell.card.get_tile_display()
                if user and cell.card in player.trap_visible.all() and cell.card.trap :
                    display = cell.card.get_trap_display()
                if cell.card in self.activated_traps.all():
                    display = cell.card.get_trap_activated_display()
                list_cards.append({'card_id': cell.card.pk, 'left': cell.get_left_offset(), 'top': cell.get_top_offset(), 'display': display, 'class': 'castlemaze-maze'})
        return list_cards

    def get_deck_cards(self):
        list_cards = []
        deck_cell = self.cell_set.filter(cell_type='deck')[0]
        for card_id in self.deck_set.get(deck_type='tile').card_order.split(';') + self.deck_set.get(deck_type='action').card_order.split(';'):
            list_cards.append({'card_id': card_id, 'left': deck_cell.get_left_offset(), 'top': deck_cell.get_top_offset(), 'display': 'img/card_back.png', 'class': 'castlemaze-card'})
        return list_cards

    def get_player_cards(self, user):
        list_cards = []
        player_tile_cards = self.player_set.get(user=user).tile_cards.all()
        player_tile_cells = self.cell_set.filter(cell_type='player_tile_hand')
        for i in range(min(len(player_tile_cards),len(player_tile_cells))):
            list_cards.append({'card_id': player_tile_cards[i].pk, 'left': player_tile_cells[i].get_left_offset(), 'top': player_tile_cells[i].get_top_offset(), 'display': player_tile_cards[i].get_card_display(),  'class': 'castlemaze-card'})
        
        player_action_cards = self.player_set.get(user=user).action_cards.all()
        player_action_cells = self.cell_set.filter(cell_type='player_action_hand')
        for i in range(min(len(player_action_cards),len(player_action_cells))):
            list_cards.append({'card_id': player_action_cards[i].pk, 'left': player_action_cells[i].get_left_offset(), 'top': player_action_cells[i].get_top_offset(), 'display': player_action_cards[i].get_card_display(),  'class': 'castlemaze-card'})
        
        
        return list_cards


    def get_other_players_cards(self, user):
        list_cards = []
        cell_red_team = self.cell_set.get(cell_type='red_team')
        cell_blue_team = self.cell_set.get(cell_type='blue_team')
        for red_player in self.player_set.filter(team='red_team'):
            if red_player.user == user:
                continue
            for card in red_player.tile_cards.all():
                list_cards.append({'card_id': card.pk, 'left': cell_red_team.get_left_offset()+100, 'top': cell_red_team.get_top_offset()+100, 'display': 'img/card_back.png',  'class': 'castlemaze-maze'})
            for card in red_player.action_cards.all():
                list_cards.append({'card_id': card.pk, 'left': cell_red_team.get_left_offset()+100, 'top': cell_red_team.get_top_offset()+100, 'display': 'img/card_back.png',  'class': 'castlemaze-maze'})
        for blue_player in self.player_set.filter(team='blue_team'):
            if blue_player.user == user:
                continue
            for card in blue_player.tile_cards.all():
                list_cards.append({'card_id': card.pk, 'left': cell_blue_team.get_left_offset()+100, 'top': cell_blue_team.get_top_offset()+100, 'display': 'img/card_back.png',  'class': 'castlemaze-maze'})
            for card in blue_player.action_cards.all():
                list_cards.append({'card_id': card.pk, 'left': cell_blue_team.get_left_offset()+100, 'top': cell_blue_team.get_top_offset()+100, 'display': 'img/card_back.png',  'class': 'castlemaze-maze'})

        return list_cards

    def get_players_pawn_positions(self):
        list_players = []
        for player in self.player_set.all():
            if player.pawn_cell:
                list_players.append({'pawn_id': player.pk, 'left': player.pawn_cell.get_left_offset(), 'top': player.pawn_cell.get_top_offset(), 'display': f'img/player_{player.team}_{player.player_id+1}.png', 'class': 'castlemaze-pawn'})
        return list_players



    def  new_deck(self):
        """ TODO adding boolean to be able to create the deck only one time """
        deck_tile = Deck(game=self)
        cards_tile = [str(card.pk) for card in list(Card.objects.filter(card_type='tile'))]
        random.shuffle(cards_tile)
        deck_tile.card_order = ';'.join(cards_tile)
        deck_tile.save()


        deck_action = Deck(game=self, deck_type='action')
        cards_action = [str(card.pk) for card in  list(Card.objects.filter(card_type='action'))]
        random.shuffle(cards_action)
        deck_action.card_order = ';'.join(cards_action)
        deck_action.save()

    def generate_cell_list(self):
        dict_castle_cards = {}
        castle_cards = Card.objects.filter(card_type='castle')
        for card in castle_cards:
            dict_castle_cards[card.img] = card
        for i in range(BOARD_WIDTH):
            for j in range(BOARD_HEIGTH):
                cell = Cell(x=i,y=j, game=self)

                if cell.x == 3 and cell.y == 4:
                    cell.card = dict_castle_cards['castle_left']
                if cell.x == 10 and cell.y == 4:
                    cell.card = dict_castle_cards['castle_right']

                cell.save()
        for i in range(NUMBER_OF_CARDS_PER_PLAYER//2):
            cell = Cell(x=i, y=0, game=self, cell_type='player_tile_hand')
            cell.save()
        for i in range(NUMBER_OF_CARDS_PER_PLAYER//2):
            cell = Cell(x=i, y=0, game=self, cell_type='player_action_hand')
            cell.save()
        cell_team_red =  Cell(x=0, y=0, game=self, cell_type='red_team')
        cell_team_red.save()
        cell_team_blue = Cell(x=0, y=0, game=self, cell_type='blue_team')
        cell_team_blue.save()
        cell = Cell(x=0, y=0, game=self, cell_type='deck')
        cell.save()
        cell_game_status = Cell(x=0,y=0, game=self, cell_type='game_status')
        cell_game_status.save()
        cell_pass = Cell(x=0, y=0, game=self, cell_type='pass_button')
        cell_pass.save()

    def draw_cards_to_players(self):
        for _ in range(NUMBER_OF_CARDS_PER_PLAYER//2):
            for player in self.player_set.all():
                card = self.deck_set.get(deck_type='tile').draw()
                if card:
                    player.tile_cards.add(card)
                    for team_player in self.player_set.filter(team=player.team):
                        team_player.trap_visible.add(card)
        for _ in range(NUMBER_OF_CARDS_PER_PLAYER//2):
            for player in self.player_set.all():
                card = self.deck_set.get(deck_type='action').draw()
                if card:
                    player.action_cards.add(card)
                    

    def start_game(self):
        if self.status != 'P':
            return
        self.status='S'
        self.save()

        for cell in self.cell_set.filter(cell_type='maze'):
            if cell.x == 0 or cell.x == BOARD_WIDTH - 1 or cell.y == 0 or cell.y == BOARD_HEIGTH - 1 or (cell.x,cell.y) in CASTLE_COORD :
                continue
            card = self.deck_set.get(deck_type='tile').draw()
            if card :
                cell.card = card
                cell.save()
        self.draw_cards_to_players()
        

        for red_player in self.player_set.filter(team='red_team'):
            cell = self.cell_set.filter(cell_type='maze', x=2, y=3+red_player.player_id)[0]
            red_player.pawn_cell = cell
            red_player.save()

        for blue_player in self.player_set.filter(team='blue_team'):
            cell = self.cell_set.filter(cell_type='maze', x=11, y=3+blue_player.player_id)[0]
            blue_player.pawn_cell = cell
            blue_player.save()
        


    def action(self, cell, user):
        # TODO verifie if that's the correct user who does the action
        if cell.cell_type != 'maze' or ( not self.card_selected and self.card_selected not in self.player_set.get(user=user).action_cards.all() \
        and self.card_selected not in self.player_set.get(user=user).tile_cards.all()):
            return
        player = self.player_set.get(user=user)
        if self.card_selected.card_type == 'action' and not player.status_played_action:
            player.remaining_moves = self.card_selected.number_of_moves
            player.status_played_action = True


        if self.card_selected.card_type == 'action' and player.remaining_moves > 0:
            self.move_player(cell, player)
            player.remaining_moves -= 1
            player.save()
        
        elif self.card_selected.card_type == 'tile' and cell.cell_type == 'maze':
            returned_card = self.move_cards(cell)
            deck_tile = self.deck_set.get(deck_type='tile')
            deck_tile.add_card(returned_card)
            player = self.player_set.get(user=user)
            player.remaining_moves = 0
            new_card = deck_tile.draw()
            player.tile_cards.add(new_card)
            for team_player in self.player_set.filter(team=player.team):
                team_player.trap_visible.add(new_card)


            player.tile_cards.remove(self.card_selected)
            for player_p in self.player_set.all():
                player_p.trap_visible.remove(returned_card)
            self.activated_traps.remove(returned_card)
            player.status_played_tile = True
            player.save()

        if player.remaining_moves <= 0 :
            if self.card_selected.card_type == 'action':
                deck_action = self.deck_set.get(deck_type='action')
                deck_action.add_card(self.card_selected)
                
                player.action_cards.add(deck_action.draw())
                player.action_cards.remove(self.card_selected)
                player.save()
            
            self.card_selected = None
            
        # we only want to check if it's a border cell
        if cell.x == 0 or cell.x == BOARD_WIDTH - 1 or cell.y == 0 or cell.y == BOARD_HEIGTH - 1:
            self.last_cell_played = cell
        blue_crown_cell = self.cell_set.get(cell_type='maze', x=10, y=4)
        red_crown_cell = self.cell_set.get(cell_type='maze', x=3, y=4)
        for red_player in self.player_set.filter(team='red_team'):
            if red_player.pawn_cell == blue_crown_cell:
                self.status='R'

        for blue_player in self.player_set.filter(team='blue_team'):
            if blue_player.pawn_cell == red_crown_cell:
                self.status='B'
        self.save()


    def move_player(self, cell_maze, player):
        
        if cell_maze.card and cell_maze.card.trap :
            for player_elem in self.player_set.all():
                if cell_maze.card not in player_elem.trap_visible.all():
                    player_elem.trap_visible.add(cell_maze.card)
            if cell_maze.card.trap == 'move':
                player.remaining_moves+=1
            if cell_maze.card.trap == 'unmove':
                player.remaining_moves -=1
            if cell_maze.card.trap == 'rotate':
                if cell_maze.card in self.activated_traps.all():
                    self.activated_traps.remove(cell_maze.card)
                else:
                    self.activated_traps.add(cell_maze.card)
            if cell_maze.card.trap == 'open':
                self.activated_traps.add(cell_maze.card)
            if cell_maze.card.trap == 'close':
                self.activated_traps.add(cell_maze.card)
            if cell_maze.card.trap == 'bombe':
                self.activated_traps.add(cell_maze.card)
                player.status_played_tile = True
                player.remaining_moves = 0
                player.save()
                return
        player.pawn_cell = cell_maze
        player.save()
        
    def move_cards(self, cell_border):

        temp_card = self.card_selected
        cell_players = []
        if cell_border.x == 0 :
            sorted_elements = sorted(self.cell_set.filter(cell_type='maze', y=cell_border.y), key=lambda a: a.x)
        elif cell_border.x == BOARD_WIDTH - 1 :
            sorted_elements = sorted(self.cell_set.filter(cell_type='maze', y=cell_border.y), key=lambda a: a.x, reverse=True)
        elif cell_border.y == 0 :
            sorted_elements = sorted(self.cell_set.filter(cell_type='maze', x=cell_border.x), key=lambda a: a.y)
        elif cell_border.y == BOARD_HEIGTH - 1 :
            sorted_elements = sorted(self.cell_set.filter(cell_type='maze', x=cell_border.x), key=lambda a: a.y, reverse=True)
        for cell in sorted_elements :
            if cell.card == None :
                continue
            temp_card, cell.card = cell.card, temp_card
            temp_players = []
            for player in cell.player_set.all():
                temp_players.append(player)
            if len(cell_players) > 0 :
                for player in cell_players :
                    player.pawn_cell = cell
                    player.save()
            cell_players = []
            for player in temp_players :
                cell_players.append(player)
            cell.save()
        return temp_card


    def get_number_of_players(self):
        return self.player_set.count()

    def get_absolute_url(self):
        return reverse("castlemaze_game", args=[self.pk])
    
    def __repr__(self):
        return self.name



class Cell(models.Model):

    """ We keep card and displayed card separated because of posible modifications of the displayed card"""
    x = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(BOARD_WIDTH-1)])
    y = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(BOARD_HEIGTH-1)])
    game = models.ForeignKey(Game, editable=False, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True)
    cell_type = models.CharField(max_length=100, default='maze')

    # TODO find a bether way to use this
    displayed_card = models.ForeignKey(Card, related_name="cell_displayed_card", on_delete=models.CASCADE, null=True)


    def get_display(self):
        if self.card is not None:
            return 'img/' + self.card.img + '.png'
        else :
            return None

    def get_left_offset(self):
        return CELL_TYPES[self.cell_type]['offset_left'] + CELL_TYPES[self.cell_type]['width'] * self.x 

    def get_top_offset(self):
        return CELL_TYPES[self.cell_type]['offset_top'] + CELL_TYPES[self.cell_type]['height'] * self.y 

    def get_class(self): 
        return CELL_TYPES[self.cell_type]['class']

