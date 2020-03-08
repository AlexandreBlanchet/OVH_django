from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy 


def login(request):
    return render(request, 'login.html', {})

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'authenticate/signup_form.html'
    success_url = reverse_lazy('tictactoe_home')