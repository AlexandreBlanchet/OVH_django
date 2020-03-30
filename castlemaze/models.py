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
    'maze' : {'offset_top': 0, 'offset_left': 0, 'width': 70, 'height': 70, 'class': 'castlemaze-maze' },
    'player_hand' : {'offset_top': 600, 'offset_left': 30, 'width': 100, 'height': 150, 'class': 'castlemaze-card' },
    'other_hands' : {'offset_top': 100, 'offset_left': 1400, 'width': 100, 'height': 150, 'class': 'castlemaze-card' },
    'deck' : {'offset_top': 0, 'offset_left': 1000, 'width': 100, 'height': 150, 'class': 'castlemaze-card' },
}

BOARD_WIDTH=14
BOARD_HEIGTH=8
NUMBER_OF_CARDS_PER_PLAYER=6

NOT_CLICKABLE_COORD = (
    (0,0),
    (0,BOARD_HEIGTH-1),
    (BOARD_WIDTH-1,0),
    (BOARD_WIDTH-1,BOARD_HEIGTH-1)
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

class GamesQuerySet(models.QuerySet):
    def games_for_user(self, user):

        return self.filter(
            Q(first_player=user) | Q(second_player=user)
        )

    def active(self):
        return self.filter(Q(status='F') | Q(status='S'))
        
class Game(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='F', choices=GAME_STATUS_CHOICES)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, null=True)
    players = models.ManyToManyField(Player)
    max_number_of_players = models.IntegerField(default=6)
    player_turn = models.IntegerField(default=0)
    objects = GamesQuerySet.as_manager()

    def board(self):
        """Return the board"""
        return self.cell_set.all()

    def get_cards_positions(self, user):
        list_cards = []
        for cell in self.cell_set.all():
            if cell.card :
                list_cards.append({'card_id': cell.card.pk, 'left': cell.get_left_offset(), 'top': cell.get_top_offset, 'display': cell.card.get_display})
        
        deck_cell = self.cell_set.filter(cell_type='deck')[0]
        for card in self.deck.cards.all() :
            list_cards.append({'card_id': card.pk, 'left': deck_cell.get_left_offset(), 'top': deck_cell.get_top_offset, 'display': card.get_display})

        player_cards = self.players.get(user=user).cards.all()
        player_cells = self.cell_set.filter(cell_type='player_hand')
        for i in range(len(player_cards)):
            list_cards.append({'card_id': player_cards[i].pk, 'left': player_cells[i].get_left_offset(), 'top': player_cells[i].get_top_offset, 'display': player_cards[i].get_display})
        
        return list_cards

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

    def draw_cards_to_players(self):
        for player in self.players.all():
            player.cards.clear()
        for _ in range(NUMBER_OF_CARDS_PER_PLAYER):
            for player in self.players.all():
                card = self.deck.draw()
                if card:
                    player.cards.add(self.deck.draw())

    def start_game(self):
        cell_content_created=[]
        for cell in self.cell_set.filter(cell_type='maze'):
            if cell.x > 0 and cell.x < BOARD_WIDTH - 1 and cell.y > 0 and cell.y < BOARD_HEIGTH - 1 :
                cell.card = self.deck.draw()
                cell.save()
                cell_content_created.append({'cell_id': cell.pk, 'card_id': cell.card.pk, 'action': 'update'})
        return cell_content_created

    def move_cards(self, card, cell_border):
        cell_list = []
        temp_card = card
        
        if cell_border.x == 0 :
            sorted_elements = sorted(self.cell_set.filter(cell_type='board', y=cell_border.y), key=lambda a: a.x)
        elif cell_border.x == BOARD_WIDTH - 1 :
            sorted_elements = sorted(self.cell_set.filter(cell_type='board', y=cell_border.y), key=lambda a: a.x, reverse=True)
        elif cell_border.y == 0 :
            sorted_elements = sorted(self.cell_set.filter(cell_type='board', x=cell_border.x), key=lambda a: a.y)
        elif cell_border.y == BOARD_HEIGTH - 1 :
            sorted_elements = sorted(self.cell_set.filter(cell_type='board', x=cell_border.x), key=lambda a: a.y, reverse=True)
        for cell in sorted_elements :
            if cell.card == None :
                continue
            cell_list.append({'cell_id': cell.pk, 'card_id': temp_card.pk, 'action': 'update'})
            
            temp_card, cell.card = cell.card, temp_card
            cell.save()
        cell_list.append({'cell_id': cell.pk, 'card_id': temp_card.pk, 'action': 'delete'})

                
        return cell_list

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
    clickable = models.BooleanField(default=False)

    # TODO find a bether way to use this
    displayed_card = models.ForeignKey(Card, related_name="cell_displayed_card", on_delete=models.CASCADE, null=True)


    def get_display(self):
        if self.card is not None:
            return 'img/' + self.card.img + '.png'
        else :
            return None

    def is_clickable(self):
        return self.clickable

    def get_left_offset(self):
        return CELL_TYPES[self.cell_type]['offset_left'] + CELL_TYPES[self.cell_type]['width'] * self.x 

    def get_top_offset(self):
        return CELL_TYPES[self.cell_type]['offset_top'] + CELL_TYPES[self.cell_type]['height'] * self.y 

    def get_class(self):
        return CELL_TYPES[self.cell_type]['class']

