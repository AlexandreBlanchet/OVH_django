from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime


DRINK_TYPE = (
    ('D', 'Drink'),
    ('W', 'Wine'),
    ('B', 'Beer'),
    ('C', 'Cocktail'),
)

class DealsQuerySet(models.QuerySet):
    def deals_for_user(self, user):
        return self.filter(
            Q(first_person=user) | Q(second_person=user)
        )

    def drinks_for_user(self, user):
        total = 0
        deals = self.filter(Q(first_person=user))
        for deal in deals:
            total += deal.get_number_of_drinks_for_first_person()
        deals = self.filter(Q(second_person=user))
        for deal in deals:
            total += deal.get_number_of_drinks_for_second_person()
        return total

    def drinks_from_user(self, user):
        total = 0
        deals = self.filter(Q(first_person=user))
        for deal in deals:
            total += deal.get_number_of_drinks_for_second_person()
        deals = self.filter(Q(second_person=user))
        for deal in deals:
            total += deal.get_number_of_drinks_for_first_person()
        return total
        
class Deal(models.Model):
    first_person = models.ForeignKey(User, related_name="first_person", on_delete=models.SET_NULL, null=True)
    second_person = models.ForeignKey(User, related_name="second_person", on_delete=models.SET_NULL, null=True, verbose_name="User to add",
        help_text="Please select the user you want to add in your list",)
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    objects = DealsQuerySet.as_manager()

    def is_in_the_deal(self, user):
        return self.first_person == user or self.second_person == user

    def new_drink(self, user):
        return Drink(deal=self, by_user=user)

    def get_number_of_drinks_for_first_person(self):
        return sum([ 1 for drink in self.drink_set.all() if drink.for_first_person and not drink.paid_time])

    def get_number_of_drinks_for_second_person(self):
        return sum([ 1 for drink in self.drink_set.all() if not drink.for_first_person and not drink.paid_time])

    def get_total_drinks(self):
        return self.drink_set.count()

    def get_drinks(self):
        return self.drink_set.all().order_by("-id")

    def __str__(self):
        return f"{self.first_person} vs {self.second_person}"

class Drink(models.Model):
    deal = models.ForeignKey(Deal, editable=False, on_delete=models.CASCADE)
    for_first_person = models.BooleanField(default=True)
    comment = models.CharField(max_length=300, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paid_time = models.DateTimeField(null = True)

    def set_paid_time(self):
        self.paid_time = datetime.now()

    