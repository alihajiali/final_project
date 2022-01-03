from typing import Generator
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template.base import Template
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy, reverse
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView
from shop.models import Category, Market, Tag, Product
from .forms import NewMarket, NewTag, NewCategory, CreateProductForm

def home(request):
    return render(request, 'shop/home.html')

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

class Admin_Store(View):
    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        if request.user == market.owner:
            return render(request, "shop/admin_store.html", {'market':market})
        return render(request, "404.html")







#                   category







class CreateTag(CreateView):
    model = Tag
    form_class = NewTag
    success_url = reverse_lazy("shop:store")

    def form_valid(self, form):
        tag = form.save(commit=False)
        market = Market.objects.get(slug=self.kwargs['slug'])
        tag_list = Tag.objects.filter(owner=market)
        for before_tag in tag_list:
            if tag.title == before_tag.title :
                return redirect("shop:show_tag", self.kwargs['slug'])
                break
        else:
            tag.owner = market
            tag.save()
            return redirect("shop:show_tag", self.kwargs['slug'])


class ShowTag(View):
    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        tags = Tag.objects.filter(owner=market)
        return render(request, "shop/table.html", {'subsets':tags, 'market':market, 'type':"tag"})


class EditTag(View):
    model = Tag
    def post(self, request, *args, **kwargs):
        tag = Tag.objects.get(id=self.kwargs['pk'])
        market = Market.objects.get(slug=self.kwargs['slug'])
        new_title = request.POST['title']

        tag_list = Tag.objects.filter(owner=market)
        for before_tag in tag_list:
            if before_tag.title == new_title :
                return redirect("shop:show_tag", self.kwargs['slug'])
                break
        else:
            tag.title = new_title
            tag.save()
            return redirect("shop:show_tag", self.kwargs['slug'])
        
    def get(self, request, *args, **kwargs):
        tag = Tag.objects.get(id=self.kwargs['pk'])
        form = NewTag(instance=tag)
        market = Market.objects.get(slug=self.kwargs['slug'])
        return render(request, "shop/edit_form.html", {'subsets':tag, 'type':"tag", 'form':form, 'market':market})


class DeleteTag(View):
    model = Tag
    def get(self, request, *args, **kwargs):
        tag = Tag.objects.get(id=self.kwargs['pk'])
        market = Market.objects.get(slug=self.kwargs['slug'])
        return render(request, "shop/delete.html", {'type_delete':'tag', 'market':market, 'tag':tag})

    def post(self, request, *args, **kwargs):
        tag = Tag.objects.get(id=self.kwargs['pk'])
        tag.delete()
        market = tag.owner
        tags = Tag.objects.filter(owner = market)
        return render(request, "shop/table.html", {'subsets':tags, 'market':market, 'type':"tag"})






#                   category







class CreateCategory(CreateView):
    model = Category
    form_class = NewCategory
    success_url = reverse_lazy("shop:store")

    def form_valid(self, form):
        category = form.save(commit=False)
        market = Market.objects.get(slug=self.kwargs['slug'])
        category_list = Category.objects.filter(owner=market)
        for before_category in category_list:
            if category.title == before_category.title :
                return redirect("shop:show_category", self.kwargs['slug'])
                break
        else:
            category.owner = market
            category.save()
            return redirect("shop:show_category", self.kwargs['slug'])


class ShowCategory(View):
    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        categorys = Category.objects.filter(owner=market)
        return render(request, "shop/table.html", {'subsets':categorys, 'market':market, 'type':"category"})


class EditCategory(View):
    model = Category
    def post(self, request, *args, **kwargs):
        category = Category.objects.get(id=self.kwargs['pk'])
        market = Market.objects.get(slug=self.kwargs['slug'])
        new_title = request.POST['title']

        category_list = Category.objects.filter(owner=market)
        for before_category in category_list:
            if before_category.title == new_title :
                return redirect("shop:show_category", self.kwargs['slug'])
                break
        else:
            category.title = new_title
            category.save()
            return redirect("shop:show_category", self.kwargs['slug'])
        
    def get(self, request, *args, **kwargs):
        category = Category.objects.get(id=self.kwargs['pk'])
        form = NewCategory(instance=category)
        market = Market.objects.get(slug=self.kwargs['slug'])
        return render(request, "shop/edit_form.html", {'subsets':category, 'type':"category", 'form':form, 'market':market})


class DeleteCategory(View):
    model = Category
    def get(self, request, *args, **kwargs):
        category = Category.objects.get(id=self.kwargs['pk'])
        market = Market.objects.get(slug=self.kwargs['slug'])
        return render(request, "shop/delete.html", {'type_delete':'category', 'market':market, 'category':category})

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(id=self.kwargs['pk'])
        category.delete()
        market = category.owner
        categorys = Category.objects.filter(owner = market)
        return render(request, "shop/table.html", {'subsets':categorys, 'market':market, 'type':"tag"})





#                    product






class CreateProduct(CreateView):
    def get(self, request, *args, **kwargs):
        form = CreateProductForm
        market = Market.objects.get(slug=self.kwargs['slug'])
        return render(request, 'shop/form.html', {'form':form, 'market':market})

    def post(self, request, *args, **kwargs):
        form = CreateProductForm(request.POST, request.FILES)
        market = Market.objects.get(slug=self.kwargs['slug'])
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = market
            product.save()
            return render(request, 'shop/form.html', {'form': form, 'market':market})
        return render(request, 'shop/form.html', {'form': form, 'market':market})