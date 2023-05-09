from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ContactForm, SignUpForm, ProductForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Product, ProductTracking
from .product_price import get_price, update_price
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import os
from dotenv import load_dotenv
load_dotenv()

# Create your views here.

@login_required(login_url='/login')
def home(request: object):
    # Get all products
    products = Product.objects.all()

    # Get sort_by parameter
    sort_by = request.GET.get("sort_by", "date_added")
    if sort_by == "name":
        products = products.order_by("name")
    elif sort_by == "price":
        products = products.order_by("price")
    else:
        products = products.order_by("-date_added")

    # Process POST request for deleting a product
    if request.method == 'POST':
        product_id = request.POST.get('product-id')
        product = Product.objects.filter(pk=product_id).first()

        # Makes sure the product exists and the user is permitted to delete it
        if product and product.author == request.user:
            product.delete()

    return render(request, 'main/index.html', {'products': products})

def signup(request: object):
    # Handles the registration of a new user
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log the user in after registration
            return redirect('/index')
    
    else:
        form = SignUpForm()
    
    return render(request, 'registration/sign-up.html', {'form': form})

@login_required(login_url='/login')
def create_product(request: object):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid(): # Make sure the form is valid
            product = form.save(commit=False) # Create a new product object but don't save it to the database until price and author is set
            product.author = request.user
            try:
                product.price = get_price(product.link) # Get the price of the product
            except:
                product.price = 0 # If the price can't be found, set it to 0, on the page it will be displayed as "N/A"
            product = product.save()
            return redirect('/index')
    
    else:
        form = ProductForm()
    
    return render(request, 'main/create-product.html', {'form': form})

@login_required(login_url='/login')
def track_product(request: object, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    tracking_entry = ProductTracking.objects.filter(user=request.user, product=product)

    if tracking_entry.exists(): # If the user is already tracking the product, delete the tracking entry
        tracking_entry.delete()
    else:
        ProductTracking.objects.create(user=request.user, product=product) # Otherwise, create a new tracking entry

    next_url = request.GET.get('next', None)

    if not next_url:
        next_url = reverse('index') #Returns the user to the previus page if there is one, otherwise the home page

    return redirect(next_url)

@login_required(login_url='/login')
def user_profile(request: object, username: str):
    user = get_object_or_404(User, username=username)
    posted_products = Product.objects.filter(author=user)
    tracked_products = Product.objects.filter(producttracking__user=user)

    # Database variables to pass to the template
    context = {
        'user_profile': user,
        'posted_products': posted_products,
        'tracked_products': tracked_products,
    }

    return render(request, 'main/user_profile.html', context)

@login_required(login_url='/login')
def edit_product(request: object, product_id: int):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.user != product.author: # Make sure the user is the author of the product
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product) # Initialize the form with the existing product data
        if form.is_valid():
            form.save() # Save the changes to the product
            return HttpResponseRedirect(reverse('user_profile', args=[request.user.username]))
    else:
        form = ProductForm(instance=product)

    # Database variables to pass to the template
    context = {
        'form': form,
        'product': product,
    }

    return render(request, 'main/edit_product.html', context)

@login_required(login_url='/login')
def edit_profile(request: object):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user) # Initialize the form with the existing user data

        if 'delete_account' in request.POST:
            request.user.delete() # Delete the user account
            return redirect('/index')

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user_profile', args=[request.user.username]))
        
    else:
        form = UserChangeForm(instance=request.user)
    
    password_change_form = PasswordChangeForm(request.user)

    # Database variables to pass to the template
    context = {
        'form': form,
        'password_change_form': password_change_form,
    }


    return render(request, 'main/edit_profile.html', context)

def about(request: object):
    return render(request, 'main/about.html')

@login_required(login_url='/login')
def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            subject = form.cleaned_data['subject'] # Get the subject and message from the form
            message = f"Message from {form.cleaned_data['name']}): {request.user.email}\n\n{form.cleaned_data['message']}"
            
            # Sends email to the admin email from the admin email
            send_mail(
                subject, 
                message, 
                settings.EMAIL_HOST_USER, 
                [settings.EMAIL_HOST_USER], 
                fail_silently=False
            )
            return HttpResponseRedirect(reverse('contact_success'))
    else:
        form = ContactForm()

    return render(request, 'main/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'main/contact_success.html')