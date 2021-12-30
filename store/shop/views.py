from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView

from shop.models import Market, Tag
from .forms import NewMarket, NewTag

def home(request):
    return render(request, 'shop/home.html')

class CreateShop(CreateView):
    model = Market
    form_class = NewMarket

    def form_valid(self, form):
        market = form.save(commit=False)
        market.owner = self.request.user
        market.save()
        return redirect("accounts:profile")
    
    def get_context_data(self,*args, **kwargs):
        context = super(self).get_context_data(*args,**kwargs)
        context['market_user'] = Market.objects.filter(owner=self.request.user)
        return context

class Admin_Store(TemplateView):
    template_name = f"shop/admin_store.html"

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        context['market'] = Market.objects.get(slug=slug)
        return context


class CreateTag(CreateView):
    model = Tag
    form_class = NewTag

    def form_valid(self, form):
        tag = form.save(commit=False)
        print("/"*80, self.slug)
        market = Market.objects.get(slug=self.slug)
        tag.owner = market
        tag.save()
        return redirect("shop:srore")