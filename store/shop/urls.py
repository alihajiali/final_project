from os import name
from django.urls import path
from . import views

app_name = 'shop' 

urlpatterns = [
    path('', views.home, name='home'),
    path('create-shop', views.CreateShop.as_view(), name='create_market'),
    path('store/<slug:slug>/', views.Admin_Store.as_view(), name='store'),
    # Tag
    path('<slug:slug>/CreateTag/', views.CreateTag.as_view(), name="CreateTag"),
    path('<slug:slug>/show_tag/', views.ShowTag.as_view(), name='show_tag'),
    path('<slug:slug>/edit_tag/<int:pk>/', views.EditTag.as_view(), name='edit_tag'),
    path('<slug:slug>/delete_tag/<int:pk>/', views.DeleteTag.as_view(), name='delete_tag'),
    # Category
    path('<slug:slug>/CreateCategory/', views.CreateCategory.as_view(), name="CreateCategory"),
    path('<slug:slug>/show_category/', views.ShowCategory.as_view(), name='show_category'),
    path('<slug:slug>/edit_category/<int:pk>/', views.EditCategory.as_view(), name='edit_category'),
    path('<slug:slug>/delete_category/<int:pk>/', views.DeleteCategory.as_view(), name='delete_category'),
    # Product
    path('<slug:slug>/create_product/', views.CreateProduct.as_view(), name='create_product'),
]