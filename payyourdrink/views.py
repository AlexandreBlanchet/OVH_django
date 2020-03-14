from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Deal
from .forms import NewDealForm
from django.core.exceptions import PermissionDenied


def welcome(request):
    if request.user.is_authenticated:
        return redirect('payyourdrink_home')
    else:
        return render(request, 'payyourdrink/welcome.html', {'app':'payyourdrink', 'appname':'Paye ton verre !'})

@login_required()
def home(request):
    my_deals = Deal.objects.deals_for_user(request.user)
    drinks_user_get = my_deals.get_drinks(request.user)
    drinks_user_give = my_deals.give_drinks(request.user)
    others_deals = my_deals.others()
    return render(request, "payyourdrink/home.html", {'drinks_user_get': drinks_user_get, 'drinks_user_give':drinks_user_give, 'others_deals':others_deals, 'app':'payyourdrink', 'appname':' Paye ton verre !'})

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
def deal_detail(request, id):
    deal = get_object_or_404(Deal, pk=id)
    return render(request, "payyourdrink/deal_details.html", {'deal': deal})


@login_required()
def change_deal(request, id):
    deal = get_object_or_404(Deal, pk=id)
    if not deal.is_in_the_deal(request.user):
        raise PermissionDenied
    drink = deal.new_drink(request.user)
    if request.POST.get('comment') is not None :
        drink.comment = request.POST.get('comment')
    if request.POST.get('give') is not None :
        drink.for_first_person = request.user.id != drink.deal.first_person.id
        drink.save()
    if request.POST.get('get') is not None :
        drink.for_first_person = request.user.id == drink.deal.first_person.id
        drink.save()
    return render(request, "payyourdrink/deal_details.html", {'deal': deal})
    #return redirect('payyourdrink_home')
