from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('index', views.home, name='index'),
    path('sign-up', views.signup, name='sign-up'),
    path('create-product', views.create_product, name='create-product'),
]