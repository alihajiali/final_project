from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from pay.models import Cart, cart_item
from shop.models import Market

class Show_panel(View):
    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        if request.user == market.owner:
            return render(request, "pay/panel.html", {'market':market})
        return render(request, "404.html")



class CartList(View):
    def get(self, request, *args, **kwargs):
        market = Market.objects.get(slug=self.kwargs['slug'])
        carts = Cart.objects.filter(market=market)
        if request.user == market.owner:
            return render(request, "pay/cart_list.html", {'market':market, 'carts':carts})
        return render(request, "404.html")



class StatusA(View):
    def post(self, request, *args, **kwargs):
        cart_id = request.POST['cart_id']
        cart = Cart.objects.get(pk=cart_id)
        cart.status = 'A'
        cart.save()
        return JsonResponse({'status':'ok'})



class StatusN(View):
    def post(self, request, *args, **kwargs):
        cart_id = request.POST['cart_id']
        cart = Cart.objects.get(pk=cart_id)
        cart.status = 'N'
        cart.save()
        return JsonResponse({'status':'ok'})



class StatusS(View):
    def post(self, request, *args, **kwargs):
        cart_id = request.POST['cart_id']
        cart = Cart.objects.get(pk=cart_id)
        cart.status = 'S'
        cart.save()
        return JsonResponse({'status':'ok'})



class ShowDetail(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(id=self.kwargs['pk'])
        item_cart = cart_item.objects.filter(cart=cart)
        market = Market.objects.get(slug=self.kwargs['slug'])
        if request.user == market.owner:
            return render(request, "pay/cart_detail.html", {'market':market, 'cart':cart, 'item_cart':item_cart})
        return render(request, "404.html")