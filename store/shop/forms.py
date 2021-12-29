from django import forms
from django.db.models import fields
from .models import Market

class NewMarket(forms.ModelForm):
    class Meta : 
        model = Market
        fields = ['title', 'slug', 'type']
