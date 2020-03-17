from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note
from datetime import datetime

def welcome(request):
    if request.user.is_authenticated:
        return redirect('keepinmind_home')
    else:
        return render(request, 'keepinmind/welcome.html', {'app':'keepinmind', 'appname':'Keep in mind !', 'footer':"You'll soon have a great mind..."})

@login_required()
def home(request):
    user_notes = Note.objects.notes_of_user(request.user)
    for note in user_notes:
        if ((datetime.now().timestamp() - note.last_active.timestamp())//3600)> note.status*2 :
            note.seen = False
            note.save()
    all_notes = user_notes.count()
    user_notes = user_notes.active()
    return render(request,'keepinmind/home.html', {'notes': user_notes,'all_notes':all_notes, 'app':'keepinmind', 'appname':'Keep in mind !', 'footer':"You'll soon have a great mind..."})

@login_required()
def edit_note(request, id):
    if id == '0' :
        note = Note(user=request.user)
    elif id == '1'  :
        notes_fact_list = Note.objects.notes_fact_list()    
        return render(request, "keepinmind/new_note_form.html", {'notes_fact_list':notes_fact_list, 'app':'keepinmind', 'appname':'Keep in mind !', 'footer':"You'll soon have a great mind..."})
    else :
        note = get_object_or_404(Note, pk=id)
    if request.method == "POST":
        if request.POST.get('delete') is not None:
            note.delete()
            return redirect('keepinmind_home')
        if request.POST.get('fact') is not None:
            note.pk = None
            note.save()
            return redirect('keepinmind_home')
        if request.POST.get('ok') is not None or request.POST.get('ko') is not None:
            note.seen = True
            note.score += 1
            if request.POST.get('ok') is not None :
                note.status *=2
            else :
                note.status /= 2
            note.save()
            return redirect('keepinmind_home')

        if request.POST.get('answer') is not None and request.POST.get('answer') != '' :
            note.is_question = True
            note.answer = request.POST.get('answer') 
        if request.POST.get('question') is not None :
            note.question = request.POST.get('question')
            note.save()
            return redirect('keepinmind_home')
    return render(request, "keepinmind/new_note_form.html", {'note':note, 'app':'keepinmind', 'appname':'Keep in mind !', 'footer':"You'll soon have a great mind..."})

