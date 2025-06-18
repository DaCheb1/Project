from django.shortcuts import render
from products.models import Product
def catalog (request):
    products = Product.objects.all()
    return render(request, 'catalog.html', {'products': products})

def catalog_detail (request, pk):
    product = Product.objects.get(pk = pk)
    return render(request, 'catalog_detail.html', {'product': product})

    