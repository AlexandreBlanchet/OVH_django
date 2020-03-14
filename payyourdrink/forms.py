from django.forms import ModelForm
from .models import Deal, User
from django.core.exceptions import ValidationError

class NewDealForm(ModelForm):
    class Meta:
        model = Deal
        fields = ['second_person']
    def __init__(self, first_person, *args, **kwargs):
        super(NewDealForm, self).__init__(*args, **kwargs)
        deals = Deal.objects.deals_for_user(first_person)
        userIds = set()
        for deal in deals :
            userIds.add(deal.first_person.id)
            userIds.add(deal.second_person.id)

        self.fields['second_person'].queryset = User.objects.exclude(pk__in=userIds)
