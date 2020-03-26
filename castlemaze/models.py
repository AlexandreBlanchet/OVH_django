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
ORIENTATIONS = (
    ('N', 'NORD'),
    ('E', 'EAST'),
    ('S', 'SOUTH'),
    ('W', 'West')
)
BOARD_SIZE=5



class Card(models.Model):
    img = models.CharField(max_length=30, default="cell.png")


class Deck(models.Model):
    number_of_cards = models.IntegerField(default=10)
    cards = models.ManyToManyField(Card)
    current_card_index = models.IntegerField(default=0)

    def draw(self):
        card = self.cards.all()[self.current_card_index]
        self.current_card_index = (self.current_card_index+1)%self.cards.count()
        self.save()
        return card

class GamesQuerySet(models.QuerySet):
    def games_for_user(self, user):

        return self.filter(
            Q(first_player=user) | Q(second_player=user)
        )

    def active(self):
        return self.filter(Q(status='F') | Q(status='S'))
        
class Game(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='F', choices=GAME_STATUS_CHOICES)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, null=True)

    objects = GamesQuerySet.as_manager()

    def board(self):
        """Return the board"""
        board = [[None for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        for cell in self.cell_set.all():
            board[cell.y][cell.x] = cell
        return board

    def  new_deck(self, number_of_cards):
        """ TODO adding boolean to be able to create the deck only one time """
        self.deck = Deck(number_of_cards=number_of_cards)
        self.deck.save()
        for i in range(number_of_cards):
            card_id = i%Card.objects.count()+1

            self.deck.cards.add(Card.objects.get(pk=card_id))
        self.deck.save()

    def generate_cell_list(self):
        for i in range(BOARD_SIZE-2):
            for j in range(BOARD_SIZE-2):
                cell = Cell(x=i+1,y=j+1, game=self, card=self.deck.draw(), card_orientation='N')
                cell.displayed_card = cell.card
                cell.save()
                
    def get_absolute_url(self):
        return reverse("castlemaze_detail", args=[self.pk])



class Cell(models.Model):

    """ We keep card and displayed card separated because of posible modifications of the displayed card"""
    x = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(BOARD_SIZE-1)])
    y = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(BOARD_SIZE-1)])
    game = models.ForeignKey(Game, editable=False, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    card_orientation = models.CharField(max_length=1, default='N', choices=ORIENTATIONS)
    displayed_card = models.ForeignKey(Card, related_name="cell_displayed_card", on_delete=models.CASCADE)

    def get_card_img(self):
        return 'img/' + self.card.img + '.png'




