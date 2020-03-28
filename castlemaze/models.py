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
        board = [[None for x in range(BOARD_WIDTH)] for y in range(BOARD_HEIGTH)]
        for cell in self.cell_set.all():
            board[cell.y][cell.x] = cell
        return board

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
                if i == 0 or i == BOARD_WIDTH - 1 or j == 0 or j == BOARD_HEIGTH - 1:
                    cell = Cell(x=i,y=j, game=self)
                    if (i,j) not in NOT_CLICKABLE_COORD:
                        cell.clickable = True
                else:
                    cell = Cell(x=i,y=j, game=self, card=self.deck.draw())
                    cell.displayed_card = cell.card
                cell.save()

    def draw_cards_to_players(self):
        for player in self.players.all():
            player.cards.clear()
        for _ in range(NUMBER_OF_CARDS_PER_PLAYER):
            for player in self.players.all():
                card = self.deck.draw()
                if card:
                    player.cards.add(self.deck.draw())

    def move_cells(self, move_cell):
        cell_list = []
        if move_cell.x == 0:
            move_cell.clickable = False
            move_cell.save()
            new_cell = Cell(x=move_cell.x,y=move_cell.y, game=self)
            Cell.objects.filter(x=BOARD_WIDTH-1, y=move_cell.y).delete()
            for cell in self.cell_set.all():
                if cell.y == move_cell.y :
                    cell.x+=1
                    cell.save()
                    cell_list.append({'cell_id':cell.pk, 'left':cell.get_left_offset(),'top':cell.get_top_offset()})
            cell = Cell.objects.filter(x=BOARD_WIDTH-1, y=move_cell.y)[0]
            self.deck.cards.add(cell.card)
            self.deck.save()
            cell.card = None
            cell.clickable = True
            cell.save()
            new_cell.clickable = True
            new_cell.save()
        if move_cell.x == BOARD_WIDTH-1:
            move_cell.clickable = False
            move_cell.save()
            new_cell = Cell(x=move_cell.x,y=move_cell.y, game=self)
            Cell.objects.filter(x=0, y=move_cell.y).delete()
            for cell in self.cell_set.all():
                if cell.y == move_cell.y :
                    cell.x-=1
                    cell.save()
                    cell_list.append({'cell_id':cell.pk, 'left':cell.get_left_offset(),'top':cell.get_top_offset()})
            cell = Cell.objects.filter(x=0, y=move_cell.y)[0]
            self.deck.cards.add(cell.card)
            self.deck.save()
            cell.card = None
            cell.clickable = True
            cell.save()
            new_cell.clickable = True
            new_cell.save()
        if move_cell.y == 0:
            move_cell.clickable = False
            move_cell.save()
            new_cell = Cell(x=move_cell.x,y=move_cell.y, game=self)
            Cell.objects.filter(x=move_cell.x, y=BOARD_HEIGTH-1).delete()
            for cell in self.cell_set.all():
                if cell.x == move_cell.x :
                    cell.y+=1
                    cell.save()
                    cell_list.append({'cell_id':cell.pk, 'left':cell.get_left_offset(),'top':cell.get_top_offset()})
            cell = Cell.objects.filter(x=move_cell.x, y=BOARD_HEIGTH-1)[0]
            self.deck.cards.add(cell.card)
            self.deck.save()
            cell.card = None
            cell.clickable = True
            cell.save()
            new_cell.clickable = True
            new_cell.save()
        if move_cell.y == BOARD_HEIGTH-1:
            move_cell.clickable = False
            move_cell.save()
            new_cell = Cell(x=move_cell.x,y=move_cell.y, game=self)
            Cell.objects.filter(x=move_cell.x, y=0).delete()
            for cell in self.cell_set.all():
                if cell.x == move_cell.x :
                    cell.y-=1
                    cell.save()
                    cell_list.append({'cell_id':cell.pk, 'left':cell.get_left_offset(),'top':cell.get_top_offset()})
            cell = Cell.objects.filter(x=move_cell.x, y=0)[0]
            self.deck.cards.add(cell.card)
            self.deck.save()
            cell.card = None
            cell.clickable = True
            cell.save()
            new_cell.clickable = True
            new_cell.save()
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
        return self.x*70

    def get_top_offset(self):
        return self.y*70

