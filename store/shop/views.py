from typing import Generator
from django.db.models.fields import mixins
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse_lazy, reverse
from django.views.generic.base import View
from django.views.generic.edit import DeleteView, UpdateView
from shop.models import Category, Market, Tag, Product
from .forms import NewTag, NewCategory, CreateProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(ListView):
    model = Product
    template_name = 'shop/home.html'
    context_object_name = 'products'
    paginate_by = 12



class Admin_Store(TemplateView):
    template_name = "shop/admin_store.html"
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['market'] = Market.objects.get(slug=self.kwargs['slug'])
        return data



#                   tag



class CreateTag(CreateView):
    model = Tag
    def post(self, request, *args, **kwargs):
        form = NewTag(request.POST)
        market = Market.objects.get(slug=self.kwargs['slug'])
        tag_list = Tag.objects.filter(owner = market)
        if form.is_valid():
            tag = form.save(commit=False)
            for before_tag in tag_list:
                if before_tag.title == tag.title:
                    break
            else:
                if request.user == market.owner:
                    tag.owner = market
                    tag.save()
        tags = Tag.objects.filter(owner = market)
        return redirect("shop:show_tag", market.slug)

    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        form = NewTag
        return render(request, "shop/tag/create_tag.html", {'market':market, 'form':form})



class ShowTag(ListView):
    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        tags = Tag.objects.filter(owner=market)

        page_num = request.GET.get('page', 1)
        paginator = Paginator(tags, 10)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "shop/tag/tag_list.html", {'market':market, 'page_obj': page_obj})



class EditTag(View):
    model = Tag

    def post(self, request, *args, **kwargs):
        tag = Tag.objects.get(id=self.kwargs['pk'])
        form = NewTag(request.POST)
        market = Market.objects.get(slug=self.kwargs['slug'])
        tag_list = Tag.objects.filter(owner = market)
        if form.is_valid():
            new_tag = form.save(commit=False)
            for before_tag in tag_list:
                if before_tag.title == new_tag.title:
                    break
            else:
                if request.user == market.owner:
                    tag.title = new_tag.title
                    tag.save()
        tags = Tag.objects.filter(owner = market)
        return redirect("shop:show_tag", market.slug)

    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        tag = Tag.objects.get(id=self.kwargs['pk'])
        form = NewTag(instance=tag)
        return render(request, "shop/tag/edit_tag.html", {'market':market, 'form':form})



class DeleteTag(View):
    model = Tag

    def get(self, request, *args, **kwargs):
        tag = Tag.objects.get(id=self.kwargs['pk'])
        market = Market.objects.get(slug=self.kwargs['slug'])
        return render(request, "shop/tag/delete_tag.html", {'market':market, 'tag':tag})

    def post(self, request, *args, **kwargs):
        tag = Tag.objects.get(id=self.kwargs['pk'])
        tag.delete()
        market = tag.owner
        tags = Tag.objects.filter(owner = market)
        return redirect("shop:show_tag", market.slug)



#                   category



class CreateCategory(CreateView):
    model = Category

    def post(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        form = NewCategory(market, request.POST)
        category_list = Category.objects.filter(owner = market)
        if form.is_valid():
            category = form.save(commit=False)
            for before_category in category_list:
                if before_category.title == category.title:
                    break
            else:
                if request.user == market.owner:
                    category.owner = market
                    category.save()
        categorys = Category.objects.filter(owner = market)
        return redirect("shop:show_category", market.slug)
        # return render(request, "shop/category/category_list.html", {'categorys':categorys, 'market':market})

    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        form = NewCategory(market)
        return render(request, "shop/category/create_category.html", {'market':market, 'form':form})



class ShowCategory(View):
    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        categorys = Category.objects.filter(owner=market)

        page_num = request.GET.get('page', 1)
        paginator = Paginator(categorys, 10)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "shop/category/category_list.html", {'market':market, 'page_obj': page_obj})



class EditCategory(View):
    model = Category

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(id=self.kwargs['pk'])
        market = Market.objects.get(slug=self.kwargs['slug'])
        form = NewCategory(market, request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            if request.user == market.owner:
                category.title = new_category.title
                category.parent = new_category.parent
                category.save()
        categorys = Category.objects.filter(owner = market)
        return redirect("shop:show_category", market.slug)

    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        category = Category.objects.get(id=self.kwargs['pk'])
        form = NewCategory(market, instance=category)
        return render(request, "shop/category/edit_category.html", {'market':market, 'form':form})



class DeleteCategory(View):
    model = Category

    def get(self, request, *args, **kwargs):
        category = Category.objects.get(id=self.kwargs['pk'])
        market = Market.objects.get(slug=self.kwargs['slug'])
        return render(request, "shop/category/delete_category.html", {'market':market, 'category':category})

    def post(self, request, *args, **kwargs):
        category = Category.objects.get(id=self.kwargs['pk'])
        category.delete()
        market = category.owner
        categorys = Category.objects.filter(owner = market)
        return redirect("shop:show_category", market.slug)



#                    product



class CreateProduct(CreateView):
    def post(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        form = CreateProductForm(market, request.POST, request.FILES)
        product_list = Product.objects.filter(market = market)
        if form.is_valid():
            product = form.save(commit=False)
            for before_product in product_list:
                if before_product.title == product.title:
                    break
            else:
                if request.user == market.owner:
                    product.market = market
                    product.save()
                    form.save_m2m()
        return redirect("shop:show_product", market.slug)

    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        form = CreateProductForm(market)
        return render(request, 'shop/product/create_product.html', {'form':form, 'market':market})


class ShowProduct(View):
    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        products = Product.objects.filter(market=market)

        page_num = request.GET.get('page', 1)
        paginator = Paginator(products, 6)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "shop/product/product_list.html", {'market':market, 'page_obj': page_obj})



class EditProduct(View):
    def post(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        product = Product.objects.get(id=self.kwargs['pk'])
        form = CreateProductForm(market, request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_product = form.save(commit=False)
            if request.user == market.owner:
                new_product.save()
                form.save_m2m()
        return redirect("shop:show_product", market.slug)

    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        product = Product.objects.get(id=self.kwargs['pk'])
        form = CreateProductForm(market, instance=product)
        return render(request, 'shop/product/edit_product.html', {'form':form, 'market':market})



class DeleteProduct(View):
    model = Product

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['pk'])
        market = Market.objects.get(slug=self.kwargs['slug'])
        return render(request, "shop/product/delete_product.html", {'market':market, 'product':product})

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['pk'])
        product.delete()
        market = product.market
        products = Product.objects.filter(market = market)
        return redirect("shop:show_product", market.slug)



class ProductDetail(DeleteView):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['pk'])
        market = product.market
        return render(request, "shop/product/product_detail.html", {'market':market, 'product':product})



class ProductLike(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=self.kwargs['pk'])
        user = request.user
        if user in product.like.all():
            product.like.remove(user)
            product.like_count -= 1
        else : 
            product.like.add(user)
            product.like_count += 1
        product.save()
        market = product.market
        return redirect("shop:product_detail", product.id)