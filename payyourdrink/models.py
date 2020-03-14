from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator

DEAL_STATUS = (
    ('F', 'Drinks for the first person'),
    ('S', 'Drinks for the second person'),
    ('N', 'No drink for either'),
)

class DealsQuerySet(models.QuerySet):
    def deals_for_user(self, user):
        return self.filter(
            Q(first_person=user) | Q(second_person=user)
        )

    def get_drinks(self, user):
        return self.filter((Q(status='F') & Q(first_person=user)) | (Q(status='S') & Q(second_person=user)))

    def give_drinks(self, user):
        return self.filter((Q(status='S') & Q(first_person=user)) | (Q(status='F') & Q(second_person=user)))

    def others(self):
        return self.filter(Q(status='N'))
        
class Deal(models.Model):
    first_person = models.ForeignKey(User, related_name="first_person", on_delete=models.SET_NULL, null=True)
    second_person = models.ForeignKey(User, related_name="second_person", on_delete=models.SET_NULL, null=True, verbose_name="User to add",
        help_text="Please select the user you want to add in your list",)
    status = models.CharField(max_length=1, default='N', choices=DEAL_STATUS)
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    objects = DealsQuerySet.as_manager()

    def is_in_the_deal(self, user):
        return self.first_person == user or self.second_person == user

    def new_drink(self, user):
        return Drink(deal=self, by_user=user)

    def get_number_of_drinks(self):
        return sum([ -1 if drink.for_first_person else 1 for drink in self.drink_set.all()])
    def get_number_of_drinks_inverse(self):
        return - sum([ -1 if drink.for_first_person else 1 for drink in self.drink_set.all()])

    def update_after_drink(self):
        if self.get_number_of_drinks() == 0 :
            self.status = 'N'
        elif self.get_number_of_drinks() > 0 :
            self.status = 'F'
        else :
            self.status = 'S'

    def get_absolute_url(self):
        return reverse("payyourdrink_detail", args=[self.pk])
    
    def __str__(self):
        return f"{self.first_person} vs {self.second_person}"

class Drink(models.Model):
    deal = models.ForeignKey(Deal, editable=False, on_delete=models.CASCADE)
    for_first_person = models.BooleanField(default=True)
    comment = models.CharField(max_length=300, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        super(Drink, self).save(*args, **kwargs)
        self.deal.update_after_drink()
        self.deal.save()
