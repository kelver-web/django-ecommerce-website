from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib import messages

from . models import Product, Category
from . forms import SignUpForm

# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def about(request):
    return render(request,'store/about.html', {})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,f'{user}, Login successfully')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
    return render(request,'store/login.html', {})


def logout_user(request):
    logout(request)
    messages.error(request, 'You have been logged out, Thanks for stopping by...')
    return redirect('login')


def register_user(request):
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created successfully. Welcome {username} !!!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below, try again...')
            return redirect('register')
    else:
        return render(request,'store/register.html', {'form':form})


def product(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'store/product.html', {'product':product})


def category(request, foo):
    # Replace Hyfens with Spaces
    foo = foo.replace('-', ' ')
    # Grab the Category from url.
    try:
        # Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request,'store/category.html', {
            'products':products,
            'category':category,})
    except:
        messages.error(request, "That Category Doesn't Exist...")
        return redirect('home')
