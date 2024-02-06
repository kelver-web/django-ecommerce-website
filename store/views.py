from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib import messages

from . models import Product
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
            messages.success(request, f'Account created for {username}, Welcome!!!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below, try again...')
            return redirect('register')
    else:
        return render(request,'store/register.html', {'form':form})

