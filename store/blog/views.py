from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic.base import View
from shop.models import Market
from .models import Post
from .forms import CreatePostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class CreatePost(CreateView):
    def post(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        form = CreatePostForm(market, request.POST, request.FILES)
        post_list = Post.objects.filter(market = market)
        if form.is_valid():
            post = form.save(commit=False)
            for before_post in post_list:
                if before_post.title == post.title:
                    break
            else:
                if request.user == market.owner:
                    post.market = market
                    post.save()
                    form.save_m2m()
        return redirect("blog:show_post", market.slug)

    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        form = CreatePostForm(market)
        return render(request, 'blog/post/create_post.html', {'form':form, 'market':market})


class ShowPost(View):
    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        posts = Post.objects.filter(market=market)

        page_num = request.GET.get('page', 1)
        paginator = Paginator(posts, 6)
        try:
            page_obj = paginator.page(page_num)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return render(request, "blog/post/post_list.html", {'market':market, 'page_obj': page_obj})



class EditPost(View):
    def post(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        post = Post.objects.get(id=self.kwargs['pk'])
        form = CreatePostForm(market, request.POST, request.FILES, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            if request.user == market.owner:
                new_post.save()
                form.save_m2m()
        return redirect("blog:show_post", market.slug)

    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        post = Post.objects.get(id=self.kwargs['pk'])
        form = CreatePostForm(market, instance=post)
        return render(request, 'blog/post/edit_post.html', {'form':form, 'market':market})



class DeletePost(View):
    model = Post

    def get(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['pk'])
        market = Market.objects.get(slug=self.kwargs['slug'])
        return render(request, "blog/post/delete_post.html", {'market':market, 'post':post})

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=self.kwargs['pk'])
        post.delete()
        market = post.market
        posts = Post.objects.filter(market = market)
        return redirect("blog:show_post", market.slug)