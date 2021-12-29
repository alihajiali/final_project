from typing import ValuesView
from django.urls import reverse_lazy, reverse
from .forms import SignUpForm
from .models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, views as auth_views
from django.views.generic import View, CreateView
from django.views.generic.edit import BaseCreateView
from django.http import HttpResponseRedirect



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


def profile(request):
    return render(request, 'accounts/profile.html')