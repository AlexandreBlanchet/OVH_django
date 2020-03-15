from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from datetime import datetime;


class NotesQuerySet(models.QuerySet):
    def notes_of_user(self, user):
        return self.filter(
            Q(user=user) 
        )

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
        return reverse("edit_note", args=[self.pk])