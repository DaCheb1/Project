from django.shortcuts import render
from products.models import Product, Category, Basket
from django.shortcuts import redirect
def catalog (request):
    category = request.GET.get('category')

    if category:
        category = int(category)

    if category:
        products = Product.objects.filter(category = category)
    else:
        products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'catalog.html', {'products': products, 'categories': categories, 'select_category': category})

def catalog_detail (request, pk):
    product = Product.objects.get(pk = pk)
    return render(request, 'catalog_detail.html', {'product': product})

def push_basket(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        if product:
            product = int(product)
        basket = Basket.objects.get(user = request.user)
        basket.products.add(Product.objects.get(id = product))
        basket.save()
        return redirect('/products/catalog/')

def basket(request):
    products = Basket.objects.get(user = request.user).products.all()
    return render(request, 'basket.html', {'products': products})
    