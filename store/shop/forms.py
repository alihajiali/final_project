from django import forms
from django.db.models import fields
from django.forms.widgets import TextInput
from .models import Tag, Product, Category



class NewTag(forms.ModelForm):
    class Meta : 
        model = Tag
        fields = ['title']

        labels = {
            "title": "عنوان تگ",
        }



class NewCategory(forms.ModelForm):
    def __init__(self, market, *args, **kwargs):
        super (NewCategory,self ).__init__(*args,**kwargs)
        self.fields['parent'].queryset = Category.objects.filter(owner=market)
    class Meta:
        model = Category
        fields = ['title', 'parent']

        labels = {
            "title": "عنوان تگ",
            "parent":"والد",
        }



class CreateProductForm(forms.ModelForm):
    def __init__(self,market, *args, **kwargs):
        super (CreateProductForm,self ).__init__(*args,**kwargs)
        if market:
            self.fields['category'].queryset = Category.objects.filter(owner=market)
            self.fields['tag'].queryset = Tag.objects.filter(owner=market)
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'number_product', 'image', 'category', 'tag', 'expire', 'status']

        labels = {
            "title": "عنوان",
            "description":"توضیحات",
            "price":"قیمت",
            "number_product":"تعداد",
            "image":"عکس",
            "category":"دسته بندی",
            "tag":"تگ",
            "expire":"تاریخ انقضا",
            "status":"وضعیت",
        }
