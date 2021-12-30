from django import forms
from django.db.models import fields
from .models import Market, Tag

class NewMarket(forms.ModelForm):
    class Meta : 
        model = Market
        fields = ['title', 'slug', 'type']


class NewTag(forms.ModelForm):
    class Meta : 
        model = Tag
        fields = ['title']