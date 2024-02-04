from django.shortcuts import render

from . models import Product

# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

# ir para a aula 05 product sales
