from urllib import request
from django.http.response import HttpResponse
from django.urls import reverse_lazy

import accounts
from .forms import SignUpForm, NewMarket, ProfileUserForm
from .models import User, Profile
from shop.models import Market
from django.shortcuts import render, redirect
from django.contrib.auth import logout, views as auth_views
from django.views.generic import View, CreateView
from django.contrib.auth.mixins import Login_is_seller_Mixin


class login(auth_views.LoginView):
    template_name = 'accounts/login.html'


class register(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_seller = True
        user.save()
        return redirect("accounts:login")



class log_out(View):
    def get(self, request):
        logout(request)
        return redirect('shop:home')


class profile(Login_is_seller_Mixin, View):
    def get(self, request, *args, **kwargs):
        try:
            market_user = Market.objects.filter(owner=self.request.user)
            profile = Profile.objects.get(user=self.request.user)
            return render(request, "accounts/profile/profile.html", {'market_user':market_user, 'profile':profile})
        except:
            form = ProfileUserForm()
            return render(request, "accounts/profile/create_profile.html", {'form':form})
    def post(self, request, *args, **kwargs):
        form = ProfileUserForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = self.request.user
            profile.save()
            form.save_m2m()
        return redirect('accounts:profile')



class EditProfile(View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        form = ProfileUserForm(instance=profile)
        return render(request, "accounts/profile/create_profile.html", {'form':form})
    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=self.request.user)
        form = ProfileUserForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = self.request.user
            profile.save()
            form.save_m2m()
        return redirect('accounts:profile')



class CreateShop(CreateView):
    model = Market
    form_class = NewMarket

    def form_valid(self, form):
        market = form.save(commit=False)
        markets = Market.objects.filter(owner=self.request.user)
        for before_market in markets:
            if before_market.title == market.title or before_market.status == 'P':
                return redirect("accounts:profile")
                break
        else :
            market.owner = self.request.user
            market.save()
            return redirect("accounts:profile")
    
    def get_context_data(self,*args, **kwargs):
        context = super(self).get_context_data(*args,**kwargs)
        context['market_user'] = Market.objects.filter(owner=self.request.user)
        return context


class EditShop(View):
    model = Market
    def post(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        new_title = request.POST['title']
        new_slug = request.POST['slug']

        markets = Market.objects.filter(owner=self.request.user)
        for before_market in markets:
            if before_market.title == new_title:
                return redirect("accounts:profile")
                break
        else :
            market.title = new_title
            market.slug = new_slug
            market.status = 'P'
            market.save()
            return redirect("accounts:profile")
        
    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        form = NewMarket(instance=market)
        market_user = Market.objects.filter(owner=self.request.user)
        return render(request, "accounts/profile/edit_shop.html", {'form':form, 'market':market, 'market_user':market_user})



class DeleteShop(View):
    model = Market
    def post(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        market.status = 'D'
        market.save()
        return redirect("accounts:profile")
        
    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        market_user = Market.objects.filter(owner=self.request.user)
        return render(request, "accounts/profile/delete_shop.html", {'market':market, 'market_user':market_user})