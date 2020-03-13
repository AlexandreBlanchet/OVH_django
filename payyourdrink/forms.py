from django.forms import ModelForm
from .models import Deal, User
from django.core.exceptions import ValidationError

class NewDealForm(ModelForm):
    class Meta:
        model = Deal
        fields = ['second_person']
    def __init__(self, first_person, *args, **kwargs):
        super(NewDealForm, self).__init__(*args, **kwargs)
        self.fields['second_person'].queryset = User.objects.exclude(pk=first_person.id)
