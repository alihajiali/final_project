from django import forms
from django.db.models import fields
from django.forms.widgets import TextInput
from .models import Post
from shop.models import Category, Tag



class CreatePostForm(forms.ModelForm):
    def __init__(self,market, *args, **kwargs):
        super (CreatePostForm,self ).__init__(*args,**kwargs)
        if market:
            self.fields['category'].queryset = Category.objects.filter(owner=market)
            self.fields['tag'].queryset = Tag.objects.filter(owner=market)
    class Meta:
        model = Post
        fields = ['title', 'description', 'main_image', 'category', 'tag', 'status']

        labels = {
            "title": "عنوان",
            "description":"توضیحات",
            "main_image":"عکس",
            "category":"دسته بندی",
            "tag":"تگ",
            "status":"وضعیت",
        }
