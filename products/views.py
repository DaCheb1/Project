from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Category, Basket
from django.contrib.auth.decorators import login_required

def catalog(request):
    category = request.GET.get('category')

    if category:
        category = int(category)

    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    
    categories = Category.objects.all()
    return render(request, 'catalog.html', {
        'products': products,
        'categories': categories,
        'select_category': category
    })

def catalog_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog_detail.html', {'product': product})

@login_required
def push_basket(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        if product_id:
            product = get_object_or_404(Product, id=int(product_id))
            basket, created = Basket.objects.get_or_create(user=request.user)
            basket.products.add(product)
            return redirect('catalog')
    return redirect('catalog')

@login_required
def basket(request):
    basket = Basket.objects.get(user=request.user)
    products = basket.products.all()
    total_price = sum(product.price for product in products)
    
    return render(request, 'basket.html', {
        'products': products,
        'total_price': total_price
    })

@login_required
def remove_from_basket(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            product = get_object_or_404(Product, id=int(product_id))
            basket = Basket.objects.get(user=request.user)
            basket.products.remove(product)
            return redirect('basket')
    return redirect('basket')

def index(request):
    return render(request, 'index.html')