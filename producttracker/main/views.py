from django.shortcuts import render, redirect
from .forms import SignUpForm, ProductForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Product
from .product_price import get_price, update_price

# Create your views here.

@login_required(login_url='/login')
def home(request):
    products = Product.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product-id')
        product = Product.objects.filter(pk=product_id).first()
        if product and product.author == request.user:
            product.delete()
        
    for product in products:
        update_price(product)

        

    return render(request, 'main/index.html', {'products': products})

def signup(request):
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
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.author = request.user
            product.price = get_price(product.link)
            product = product.save()
            return redirect('/index')
    
    else:
        form = ProductForm()
    
    return render(request, 'main/create-product.html', {'form': form})