from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .forms import SignUpForm, ProductForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Product, ProductTracking
from .product_price import get_price, update_price
from django.contrib.auth.models import User
from urllib.parse import urlparse, urlunparse
from django.urls import reverse

# Create your views here.

@login_required(login_url='/login')
def home(request: object):
    products = Product.objects.all()
    
    sort_by = request.GET.get("sort_by", "date_added")
    if sort_by == "name":
        products = products.order_by("name")
    elif sort_by == "price":
        products = products.order_by("price")
    else:  # Default sorting: date_added
        products = products.order_by("-date_added")

    if request.method == 'POST':
        product_id = request.POST.get('product-id')
        product = Product.objects.filter(pk=product_id).first()
        if product and product.author == request.user:
            product.delete()
        
    for product in products:
        update_price(product)

        

    return render(request, 'main/index.html', {'products': products})

def signup(request: object):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/index')
    
    else:
        form = SignUpForm()
    
    return render(request, 'registration/sign-up.html', {'form': form})

@login_required(login_url='/login')
def create_product(request: object):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            try:
                product.price = get_price(product.link)
            except:
                product.price = 0
            product = product.save()
            return redirect('/index')
    
    else:
        form = ProductForm()
    
    return render(request, 'main/create-product.html', {'form': form})

@login_required(login_url='/login')
def track_product(request: object, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    tracking_entry = ProductTracking.objects.filter(user=request.user, product=product)

    if tracking_entry.exists():
        tracking_entry.delete()
    else:
        ProductTracking.objects.create(user=request.user, product=product)

    next_url = request.GET.get('next', None)
    if not next_url:
        next_url = reverse('index')
    return redirect(next_url)

@login_required(login_url='/login')
def user_profile(request: object, username: str):
    user = get_object_or_404(User, username=username)
    posted_products = Product.objects.filter(author=user)
    tracked_products = Product.objects.filter(producttracking__user=user)

    context = {
        'user_profile': user,
        'posted_products': posted_products,
        'tracked_products': tracked_products,
    }

    return render(request, 'main/user_profile.html', context)

@login_required(login_url='/login')
def edit_product(request: object, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.user != product.author:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user_profile', args=[request.user.username]))
    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
    }

    return render(request, 'main/edit_product.html', context)

@login_required(login_url='/login')
def edit_profile(request: object):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)

        if 'delete_account' in request.POST:
            request.user.delete()
            return HttpResponseRedirect(reverse('home'))

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user_profile', args=[request.user.username]))
        
    else:
        form = UserChangeForm(instance=request.user)
    
    password_change_form = PasswordChangeForm(request.user)

    context = {
        'form': form,
        'password_change_form': password_change_form,
    }


    return render(request, 'main/edit_profile.html', context)