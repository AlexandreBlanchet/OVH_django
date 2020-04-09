from castlemaze.models import Card

# Delete existing cards

Card.objects.all().delete()

# Tile cards


for _ in range(30):
    card = Card()
    card.img = 'shape_1'
    card.card_type = 'tile'
    card.trap = ''
    card.open_top = True
    card.open_left = False
    card.open_bottom = True
    card.open_right = False
    card.number_of_moves = 0
    card.save()

for _ in range(5):
    card = Card()
    card.img = 'shape_1'
    card.card_type = 'tile'
    card.trap = 'rotate'
    card.open_top = True
    card.open_left = False
    card.open_bottom = True
    card.open_right = False
    card.activated_open_top = False
    card.activated_open_left = True
    card.activated_open_bottom = False
    card.activated_open_right = True
    card.number_of_moves = 0
    card.save()


for _ in range(2):
    card = Card()
    card.img = 'shape_1'
    card.card_type = 'tile'
    card.trap = 'move'
    card.open_top = True
    card.open_left = False
    card.open_bottom = True
    card.open_right = False
    card.number_of_moves = 0
    card.save()


for _ in range(30):
    card = Card()
    card.img = 'shape_1_2'
    card.card_type = 'tile'
    card.open_top = False
    card.open_left = True
    card.open_bottom = False
    card.open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(5):
    card = Card()
    card.img = 'shape_1_2'
    card.card_type = 'tile'
    card.trap = 'rotate'
    card.open_top = False
    card.open_left = True
    card.open_bottom = False
    card.open_right = True
    card.activated_open_top = True
    card.activated_open_left = False
    card.activated_open_bottom = True
    card.activated_open_right = False
    card.number_of_moves = 0
    card.save()

for _ in range(2):
    card = Card()
    card.img = 'shape_1_2'
    card.card_type = 'tile'
    card.trap = 'move'
    card.open_top = False
    card.open_left = True
    card.open_bottom = False
    card.open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(15):
    card = Card()
    card.img = 'shape_2'
    card.card_type = 'tile'
    card.open_top = True
    card.open_left = False
    card.open_bottom = True
    card.open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(3):
    card = Card()
    card.img = 'shape_2'
    card.card_type = 'tile'
    card.trap = 'open'
    card.open_top = True
    card.open_left = False
    card.open_bottom = True
    card.open_right = True
    card.activated_open_top = True
    card.activated_open_left = True
    card.activated_open_bottom = True
    card.activated_open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(3):
    card = Card()
    card.img = 'shape_2'
    card.card_type = 'tile'
    card.trap = 'close'
    card.open_top = True
    card.open_left = False
    card.open_bottom = True
    card.open_right = True
    card.activated_open_top = True
    card.activated_open_left = False
    card.activated_open_bottom = True
    card.activated_open_right = False
    card.number_of_moves = 0
    card.save()


for _ in range(15):
    card = Card()
    card.img = 'shape_2_2'
    card.card_type = 'tile'
    card.open_top = False
    card.open_left = True
    card.open_bottom = True
    card.open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(3):
    card = Card()
    card.img = 'shape_2_2'
    card.card_type = 'tile'
    card.trap = 'open'
    card.open_top = False
    card.open_left = True
    card.open_bottom = True
    card.open_right = True
    card.activated_open_top = True
    card.activated_open_left = True
    card.activated_open_bottom = True
    card.activated_open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(3):
    card = Card()
    card.img = 'shape_2_2'
    card.card_type = 'tile'
    card.trap = 'close'
    card.open_top = False
    card.open_left = True
    card.open_bottom = True
    card.open_right = True
    card.activated_open_top = False
    card.activated_open_left = True
    card.activated_open_bottom = False
    card.activated_open_right = True
    card.number_of_moves = 0
    card.save()


for _ in range(15):
    card = Card()
    card.img = 'shape_2_3'
    card.card_type = 'tile'
    card.open_top = True
    card.open_left = True
    card.open_bottom = True
    card.open_right = False
    card.number_of_moves = 0
    card.save()

for _ in range(2):
    card = Card()
    card.img = 'shape_2_3'
    card.card_type = 'tile'
    card.trap = 'open'
    card.open_top = True
    card.open_left = True
    card.open_bottom = True
    card.open_right = False
    card.activated_open_top = True
    card.activated_open_left = True
    card.activated_open_bottom = True
    card.activated_open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(2):
    card = Card()
    card.img = 'shape_2_3'
    card.card_type = 'tile'
    card.trap = 'close'
    card.open_top = True
    card.open_left = True
    card.open_bottom = True
    card.open_right = False
    card.activated_open_top = True
    card.activated_open_left = False
    card.activated_open_bottom = True
    card.activated_open_right = False
    card.number_of_moves = 0
    card.save()


for _ in range(15):
    card = Card()
    card.img = 'shape_2_4'
    card.card_type = 'tile'
    card.open_top = True
    card.open_left = True
    card.open_bottom = False
    card.open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(2):
    card = Card()
    card.img = 'shape_2_4'
    card.card_type = 'tile'
    card.trap = 'open'
    card.open_top = True
    card.open_left = True
    card.open_bottom = False
    card.open_right = True
    card.activated_open_top = True
    card.activated_open_left = True
    card.activated_open_bottom = True
    card.activated_open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(2):
    card = Card()
    card.img = 'shape_2_4'
    card.card_type = 'tile'
    card.trap = 'close'
    card.open_top = True
    card.open_left = True
    card.open_bottom = False
    card.open_right = True
    card.activated_open_top = False
    card.activated_open_left = True
    card.activated_open_bottom = False
    card.activated_open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(60):
    card = Card()
    card.img = 'shape_3'
    card.card_type = 'tile'
    card.open_top = True
    card.open_left = True
    card.open_bottom = True
    card.open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(6):
    card = Card()
    card.img = 'shape_3'
    card.card_type = 'tile'
    card.trap = 'move'
    card.open_top = True
    card.open_left = True
    card.open_bottom = True
    card.open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(10):
    card = Card()
    card.img = 'shape_3'
    card.card_type = 'tile'
    card.trap = 'unmove'
    card.open_top = True
    card.open_left = True
    card.open_bottom = True
    card.open_right = True
    card.number_of_moves = 0
    card.save()

for _ in range(10):
    card = Card()
    card.img = 'shape_3'
    card.card_type = 'tile'
    card.trap = 'bombe'
    card.open_top = True
    card.open_left = True
    card.open_bottom = True
    card.open_right = True
    card.activated_open_top = False
    card.activated_open_left = False
    card.activated_open_bottom = False
    card.activated_open_right = False
    card.number_of_moves = 0
    card.save()

for _ in range(15):
    card = Card()
    card.img = 'shape_4'
    card.card_type = 'tile'
    card.open_top = True
    card.open_left = False
    card.open_bottom = False
    card.open_right = True
    card.number_of_moves = 0
    card.save()


for _ in range(15):
    card = Card()
    card.img = 'shape_4_2'
    card.card_type = 'tile'
    card.open_top = False
    card.open_left = False
    card.open_bottom = True
    card.open_right = True
    card.number_of_moves = 0
    card.save()


for _ in range(15):
    card = Card()
    card.img = 'shape_4_3'
    card.card_type = 'tile'
    card.open_top = False
    card.open_left = True
    card.open_bottom = True
    card.open_right = False
    card.number_of_moves = 0
    card.save()


for _ in range(15):
    card = Card()
    card.img = 'shape_4_4'
    card.card_type = 'tile'
    card.open_top = True
    card.open_left = True
    card.open_bottom = False
    card.open_right = False
    card.number_of_moves = 0
    card.save()

# Action cards

for _ in range(40):
    card = Card()
    card.img = 'action_1'
    card.card_type = 'action'
    card.open_top = False
    card.open_left = False
    card.open_bottom = False
    card.open_right = False
    card.number_of_moves = 1
    card.save()


for _ in range(40):
    card = Card()
    card.img = 'action_2'
    card.card_type = 'action'
    card.open_top = False
    card.open_left = False
    card.open_bottom = False
    card.open_right = False
    card.number_of_moves = 2
    card.save()


for _ in range(30):
    card = Card()
    card.img = 'action_3'
    card.card_type = 'action'
    card.open_top = False
    card.open_left = False
    card.open_bottom = False
    card.open_right = False
    card.number_of_moves = 3
    card.save()

# Castle card

card = Card()
card.img = 'castle_left'
card.card_type = 'castle'
card.open_top = False
card.open_left = True
card.open_bottom = False
card.open_right = False
card.number_of_moves = 0
card.save()


card = Card()
card.img = 'castle_right'
card.card_type = 'castle'
card.open_top = False
card.open_left = False
card.open_bottom = False
card.open_right = True
card.number_of_moves = 0
card.save()
