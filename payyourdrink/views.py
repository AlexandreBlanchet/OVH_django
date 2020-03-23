from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Deal, Drink
from .forms import NewDealForm
from django.core.exceptions import PermissionDenied


def welcome(request):
    if request.user.is_authenticated:
        return redirect('payyourdrink_home')
    else:
        return render(request, 'payyourdrink/welcome.html', {'app':'payyourdrink', 'appname':'Have a drink !', 'footer':"It's always a pleasure to have a drink..."})

@login_required()
def home(request):
    my_deals = Deal.objects.deals_for_user(request.user)
    total_drinks_to_get = Deal.objects.drinks_for_user(request.user)
    total_drinks_to_give = Deal.objects.drinks_from_user(request.user)
    return render(request, "payyourdrink/home.html", {'deals': my_deals, 'total_drinks_to_get':total_drinks_to_get,'total_drinks_to_give':total_drinks_to_give, 'app':'payyourdrink', 'appname':'Have a drink !', 'footer':"It's always a pleasure to have a drink..."})

@login_required()
def new_deal(request):
    if request.method == "POST":
        new_deal = Deal(first_person=request.user)
        form = NewDealForm(request.user, instance=new_deal, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('payyourdrink_home')
    else:
        form = NewDealForm(request.user)
    return render(request, "payyourdrink/new_deal_form.html", {'form':form})
   

@login_required()
def change_deal(request, id):
    deal = get_object_or_404(Deal, pk=id)
    if not deal.is_in_the_deal(request.user):
        raise PermissionDenied
    drink = deal.new_drink(request.user)
    if request.POST.get('comment') is not None :
        drink.comment = request.POST.get('comment')
    if request.POST.get('get') is not None :
        drink.for_first_person = request.user.id != drink.deal.first_person.id
        drink.save()
    elif request.POST.get('give') is not None :
        drink.for_first_person = request.user.id == drink.deal.first_person.id
        drink.save()
    elif request.POST.get('paid') is not None :
        drink.set_paid_time()
        drink.save()
    return redirect('payyourdrink_home')

@login_required()
def update_drink(request, id):
    drink = get_object_or_404(Drink, pk=id)
    if not drink.deal.is_in_the_deal(request.user):
        raise PermissionDenied
    drink.set_paid_time()
    drink.save()
    return redirect('payyourdrink_home')