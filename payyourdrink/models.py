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

    def get(self, user):
        return self.filter((Q(status='F') & Q(first_person=user)) | (Q(status='S') & Q(second_person=user)))

    def give(self, user):
        return self.filter((Q(status='S') & Q(first_person=user)) | (Q(status='F') & Q(second_person=user)))

    def others(self):
        return self.filter(Q(status='N'))
        
class Deal(models.Model):
    first_person = models.ForeignKey(User, related_name="first_person", on_delete=models.SET_NULL, null=True)
    second_person = models.ForeignKey(User, related_name="second_person", on_delete=models.SET_NULL, null=True, verbose_name="User to add",
        help_text="Please select the user you want to add in your list",)
    number_of_drinks = models.IntegerField( validators=[MinValueValidator(0),MaxValueValidator(100)], default=0)
    status = models.CharField(max_length=1, default='N', choices=DEAL_STATUS)
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    objects = DealsQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse("tictactoe_detail", args=[self.pk])

    def add_drink(self):
        self.number_of_drinks+=1
        self.status='S'
        self.save()
        return reverse("payyourdrink_home")

    def remove_drink(self):
        self.number_of_drinks-=1
        self.save()
        return reverse("payyourdrink_home")
    
    def __str__(self):
        return f"{self.first_person} vs {self.second_person}"
