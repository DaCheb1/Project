from django.shortcuts import render
from products.models import Product, Category
def catalog (request):
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category = category)
    else:
        products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'catalog.html', {'products': products, 'categories': categories, 'select_category': category})

def catalog_detail (request, pk):
    product = Product.objects.get(pk = pk)
    return render(request, 'catalog_detail.html', {'product': product})

    