from django.shortcuts import render
from products.models import Product
def catalog (request):
    products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products})