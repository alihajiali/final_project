from django import forms
from django.db.models import fields
from django.forms.widgets import TextInput
from .models import Market, Tag, Product

class NewMarket(forms.ModelForm):
    class Meta : 
        model = Market
        fields = ['title', 'slug', 'type']


class NewTag(forms.ModelForm):
    class Meta : 
        model = Tag
        fields = ['title']

        labels = {
            "title": "عنوان تگ",
        }


class NewCategory(forms.ModelForm):
    class Meta : 
        model = Tag
        # fields = ['parent', 'title']
        fields = ['title']

        labels = {
            "title": "عنوان تگ",
            # "parent": "والد",
        }

class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'number_product', 'image', 'category', 'tag', 'expire', 'status']
