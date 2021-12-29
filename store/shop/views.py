from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse

from shop.models import Market
from .forms import NewMarket

def home(request):
    return render(request, 'shop/home.html')

class CreateShop(CreateView):
    model = Market
    form_class = NewMarket

    def form_valid(self, form):
        market = form.save(commit=False)
        market.owner = self.request.user
        market_user = Market.objects.filter(owner=self.request.user)
        market.save()
        return redirect("accounts:profile")