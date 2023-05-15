from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('index', views.home, name='index'),
    path('sign-up', views.signup, name='sign-up'),
    path('create-product', views.create_product, name='create-product'),
    path('track_product/<int:product_id>/', views.track_product, name='track_product'),
    path('user_profile/<str:username>/', views.user_profile, name='user_profile'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact_success/', views.contact_success, name='contact_success'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
]