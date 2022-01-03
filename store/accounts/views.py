from django.urls import reverse_lazy
from .forms import SignUpForm
from .models import User
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
        market_user = Market.objects.filter(owner=self.request.user)
        return render(request, "accounts/profile.html", {'market_user':market_user})