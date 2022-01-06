from os import name
from django.urls import path
from . import views

app_name = 'blog' 

urlpatterns = [
    path('<slug:slug>/create_post/', views.CreatePost.as_view(), name='create_post'),
    path('<slug:slug>/show_post/', views.ShowPost.as_view(), name='show_post'),
    path('<slug:slug>/edit_post/<int:pk>/', views.EditPost.as_view(), name='edit_post'),
    path('<slug:slug>/delete_post/<int:pk>/', views.DeletePost.as_view(), name='delete_post'),
]