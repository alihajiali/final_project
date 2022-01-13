from os import name
from django.urls import path
from . import views

app_name = 'shop' 

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('store/<slug:slug>/', views.Admin_Store.as_view(), name='store'),
    # Tag
    path('<slug:slug>/create_tag/', views.CreateTag.as_view(), name="create_tag"),
    path('<slug:slug>/show_tag/', views.ShowTag.as_view(), name='show_tag'),
    path('<slug:slug>/edit_tag/<int:pk>/', views.EditTag.as_view(), name='edit_tag'),
    path('<slug:slug>/delete_tag/<int:pk>/', views.DeleteTag.as_view(), name='delete_tag'),
    # Category
    path('<slug:slug>/create_category/', views.CreateCategory.as_view(), name="create_category"),
    path('<slug:slug>/show_category/', views.ShowCategory.as_view(), name='show_category'),
    path('<slug:slug>/edit_category/<int:pk>/', views.EditCategory.as_view(), name='edit_category'),
    path('<slug:slug>/delete_category/<int:pk>/', views.DeleteCategory.as_view(), name='delete_category'),
    # Product
    path('<slug:slug>/create_product/', views.CreateProduct.as_view(), name='create_product'),
    path('<slug:slug>/show_product/', views.ShowProduct.as_view(), name='show_product'),
    path('<slug:slug>/edit_product/<int:pk>/', views.EditProduct.as_view(), name='edit_product'),
    path('<slug:slug>/delete_product/<int:pk>/', views.DeleteProduct.as_view(), name='delete_product'),
    path('product_detail/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('product_like/<int:pk>/', views.ProductLike.as_view(), name='product_like'),
]