from django.forms import ModelForm
from .models import Invitation, Move, User
from django.core.exceptions import ValidationError

class InvitationForm(ModelForm):
    class Meta:
        model = Invitation
        exclude = ('from_user', 'timestamp')
    def __init__(self, from_user, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.fields['to_user'].queryset = User.objects.exclude(pk=from_user.id)


class MoveForm(ModelForm):
    class Meta:
        model = Move
        exclude = []
    
    def clean(self):
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        game = self.instance.game
        try : 
            if game.board()[y][x] is not None:
                raise ValidationError('Square is not empty')
        except IndexError:
            raise ValidationError('Invalid coordinates')
        return self.cleaned_data