from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Deal
from .forms import NewDealForm


def welcome(request):
    if request.user.is_authenticated:
        return redirect('payyourdrink_home')
    else:
        return render(request, 'payyourdrink/welcome.html', {'app':'payyourdrink', 'appname':'Paye ton verre !'})

@login_required()
def home(request):
    my_deals = Deal.objects.deals_for_user(request.user)
    drinks_user_get = my_deals.get(request.user)
    drinks_user_give = my_deals.give(request.user)
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
   