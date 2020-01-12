from django.shortcuts import render
from django.contrib.auth import authenticate, login

def serverChat(request):
    return render(request, 'home.html', {})