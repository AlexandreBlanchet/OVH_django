from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from django.conf import settings


class NotesQuerySet(models.QuerySet):
    def notes_of_user(self, user):
        return self.filter(Q(user=user))

    def notes_fact_list(self):
        user = User.objects.get(username=settings.FACT_USERNAME)
        return self.filter(Q(user=user))

    def active(self):
        return self.filter(Q(seen=False))

class Note(models.Model):
    user = models.ForeignKey(User, related_name="User", on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    is_question = models.BooleanField(default=False)
    question = models.CharField(max_length=500)
    answer = models.CharField(max_length=500, blank=True)
    status = models.IntegerField(default=1)
    score = models.IntegerField(default=0)
    seen = models.BooleanField(default=False)
    
    objects = NotesQuerySet.as_manager()

    def get_absolute_url(self):
        if self.pk is None :
            return reverse("keepinmind_edit_note", args=[0])
        return reverse("keepinmind_edit_note", args=[self.pk])
        
    def is_owner(self, user):
        return self.user == user

    def get_is_question_first(self):
        return self.score%2 == 0