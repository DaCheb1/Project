from django.shortcuts import render
from products.models import Product, Category

def index(request):
    # Получаем популярные товары для главной страницы
    popular_products = Product.objects.all()[:8]
    
    # Получаем категории для быстрого доступа
    categories = Category.objects.all()[:6]
    
    return render(request, 'index.html', {
        'popular_products': popular_products,
        'categories': categories
    })