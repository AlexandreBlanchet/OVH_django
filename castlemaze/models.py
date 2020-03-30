from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

GAME_STATUS_CHOICES = (
    ('F', 'First player to move'),
    ('S', 'Second player to move'),
    ('W', 'First player wins'),
    ('L', 'Second player wins'),
    ('D', 'Draw')
)

CELL_TYPES = {
    'maze' : {'offset_top': 20, 'offset_left': 20, 'width': 60, 'height': 60, 'class': 'castlemaze-maze' },
    'player_hand' : {'offset_top': 400, 'offset_left': 900, 'width': 100, 'height': 150, 'class': 'castlemaze-card' },
    'other_hands' : {'offset_top': 100, 'offset_left': 1300, 'width': 100, 'height': 150, 'class': 'castlemaze-card' },
    'deck' : {'offset_top': 10, 'offset_left': 1000, 'width': 100, 'height': 150, 'class': 'castlemaze-card' },
}

BOARD_WIDTH=14
BOARD_HEIGTH=9
NUMBER_OF_CARDS_PER_PLAYER=6

NOT_CLICKABLE_COORD = (
    (0,0),
    (0,BOARD_HEIGTH-1),
    (BOARD_WIDTH-1,0),
    (BOARD_WIDTH-1,BOARD_HEIGTH-1),
    (0,3),
    (0,4),
    (0,5),
    (BOARD_WIDTH-1,3),
    (BOARD_WIDTH-1,4),
    (BOARD_WIDTH-1,5),
    (3,0),
    (3,BOARD_HEIGTH-1),
    (10,0),
    (10,BOARD_HEIGTH-1),
)

CASTLE_COORD = (
    (3,3),
    (3,4),
    (3,5),
    (10,3),
    (10,4),
    (10,5),
)

class Card(models.Model):
    img = models.CharField(max_length=30, default="cell.png")

    def get_display(self):
        return 'img/'+self.img+'.png'
    

class Deck(models.Model):
    cards = models.ManyToManyField(Card)

    def draw(self):
        card = None
        if self.cards.count() > 0:
            card = self.cards.all()[0]
            self.cards.remove(card)
        return card

class Player(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card)
    cell = models.ForeignKey('Cell', on_delete=models.CASCADE, null = True)

class Game(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='F', choices=GAME_STATUS_CHOICES)
    card_selected = models.ForeignKey(Card, on_delete=models.CASCADE, null=True)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, null=True)
    players = models.ManyToManyField(Player)
    max_number_of_players = models.IntegerField(default=6)
    player_turn = models.IntegerField(default=0)

    def board(self):
        return self.cell_set.all()

    def get_board(self, user):
        """Return the board"""
        board = {}
        board['cells'] = self.get_cells(user)
        board['cards'] = self.get_cards_positions(user)
        board['players'] = self.get_players_positions()
        return board


    def get_cells(self, user):
        # TODO getting only modified cards
        cells = []
        for cell in self.cell_set.all() :
            clickable = False
            click_class = ''
            if not self.card_selected and cell.cell_type == 'player_hand':
                clickable = True
                click_class = ' clickable'
            if self.card_selected and cell.cell_type == 'maze' and (cell.x == 0 or cell.x == BOARD_WIDTH - 1 or cell.y == 0 or cell.y == BOARD_HEIGTH - 1):
                clickable = True
                click_class = ' clickable'
            if (cell.x, cell.y) in NOT_CLICKABLE_COORD and cell.cell_type == 'maze' :
                clickable = False
                click_class = ''

            cells.append({'cell_id':cell.pk, 'clickable': clickable, 'class' : cell.get_class() + click_class, 'left': cell.get_left_offset(), 'top': cell.get_top_offset()})
        return cells

    def get_cards_positions(self, user):
        list_cards = []
        for cell in self.cell_set.all():
            if cell.card :
                list_cards.append({'card_id': cell.card.pk, 'left': cell.get_left_offset(), 'top': cell.get_top_offset(), 'display': cell.card.get_display()})
        
        deck_cell = self.cell_set.filter(cell_type='deck')[0]
        for card in self.deck.cards.all() :
            list_cards.append({'card_id': card.pk, 'left': deck_cell.get_left_offset(), 'top': deck_cell.get_top_offset(), 'display': card.get_display()})

        player_cards = self.players.get(user=user).cards.all()
        player_cells = self.cell_set.filter(cell_type='player_hand')
        for i in range(len(player_cards)):
            list_cards.append({'card_id': player_cards[i].pk, 'left': player_cells[i].get_left_offset(), 'top': player_cells[i].get_top_offset(), 'display': player_cards[i].get_display()})
        
        return list_cards

    def get_players_positions(self):
        list_players = []
        for player in self.players.all():
            if player.cell:
                list_players.append({'player_id': player.pk, 'left': player.cell.get_left_offset(), 'top': player.cell.get_top_offset(), 'display': 'img/player_1.png'})
        return list_players



    def  new_deck(self):
        """ TODO adding boolean to be able to create the deck only one time """
        deck = Deck()
        deck.save()

        self.deck = deck
        for i in range(Card.objects.count()):
            deck.cards.add(Card.objects.get(pk=i+1))
        deck.save()

    def generate_cell_list(self):
        for i in range(BOARD_WIDTH):
            for j in range(BOARD_HEIGTH):
                cell = Cell(x=i,y=j, game=self)
                cell.save()
        for i in range(NUMBER_OF_CARDS_PER_PLAYER):
            cell = Cell(x=i, y=0, game=self, cell_type='player_hand')
            cell.save()
        for i in range(self.players.count()-1):
            cell = Cell(x=0, y=i, game=self, cell_type='other_hands')
            cell.save()
        cell = Cell(x=0, y=0, game=self, cell_type='deck')
        cell.save()
        for player in self.players.all():
            player.cell = cell
            player.save()

    def draw_cards_to_players(self):
        for player in self.players.all():
            player.cards.clear()
        for _ in range(NUMBER_OF_CARDS_PER_PLAYER):
            for player in self.players.all():
                card = self.deck.draw()
                if card:
                    player.cards.add(self.deck.draw())

    def start_game(self):
        self.draw_cards_to_players()
        
        player = self.players.all()[0]
        cell = self.cell_set.filter(cell_type='maze', x=6, y=2)[0]
        player.cell = cell
        player.save()
        self.save()
        for cell in self.cell_set.filter(cell_type='maze'):
            if cell.x == 0 or cell.x == BOARD_WIDTH - 1 or cell.y == 0 or cell.y == BOARD_HEIGTH - 1 or (cell.x,cell.y) in CASTLE_COORD :
                continue
            card = self.deck.draw()
            if card :
                cell.card = card
                cell.save()

    def move_cards(self, cell_border, user):
        if not self.card_selected :
            return
        self.players.get(user=user).cards.remove(self.card_selected)
        temp_card = self.card_selected
        cell_players = []
        self.card_selected = None
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
                    player.cell = cell
                    player.save()
            cell_players = []
            for player in temp_players :
                cell_players.append(player)
            cell.save()
        self.deck.cards.add(temp_card)
        self.save()

    def get_number_of_players(self):
        return self.players.count()

    def get_player_cards(self, user):
        return self.players.get(user=user).cards.all()
        
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

