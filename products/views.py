from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Basket, BasketItem

def catalog(request):
    # Получаем параметры фильтрации
    category_id = request.GET.get('category')
    search_query = request.GET.get('search', '').strip()
    
    # Начинаем с всех товаров
    products = Product.objects.all()
    
    # Фильтрация по категории
    selected_category = None
    if category_id and category_id != 'all':
        try:
            category_id = int(category_id)
            products = products.filter(category_id=category_id)
            selected_category = Category.objects.get(id=category_id)
        except (ValueError, Category.DoesNotExist):
            selected_category = None
    
    # Поиск по названию и описанию
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | 
            Q(desc__icontains=search_query)
        )
    
    # Получаем все категории для фильтра
    categories = Category.objects.all()
    
    # Считаем количество товаров в каждой категории
    category_counts = []
    for cat in categories:
        count = Product.objects.filter(category=cat).count()
        category_counts.append({
            'category': cat,
            'count': count
        })
    
    # Общее количество всех товаров
    total_count = Product.objects.count()
    
    return render(request, 'catalog.html', {
        'products': products,
        'categories': categories,
        'category_counts': category_counts,
        'selected_category': selected_category,
        'search_query': search_query,
        'products_count': products.count(),
        'total_count': total_count,
    })

def catalog_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Получаем похожие товары из той же категории
    similar_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    return render(request, 'catalog_detail.html', {
        'product': product,
        'similar_products': similar_products
    })

@login_required
def push_basket(request):
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = int(request.POST.get('quantity', 1))
        next_url = request.POST.get('next')
        
        if not next_url or next_url == 'None':
            # Если next_url не передан, возвращаемся на страницу, с которой пришли
            referer = request.META.get('HTTP_REFERER')
            if referer:
                next_url = referer
            else:
                next_url = 'catalog'
        
        if product_id:
            product = get_object_or_404(Product, id=int(product_id))
            basket, created = Basket.objects.get_or_create(user=request.user)
            
            # Проверяем, есть ли уже такой товар в корзине
            basket_item = BasketItem.objects.filter(basket=basket, product=product).first()
            
            if basket_item:
                # Если товар уже есть, увеличиваем количество
                basket_item.quantity += quantity
                basket_item.save()
                messages.success(request, f'✅ Количество товара "{product.title}" увеличено до {basket_item.quantity}!')
            else:
                # Если товара нет, создаем новую запись
                BasketItem.objects.create(basket=basket, product=product, quantity=quantity)
                messages.success(request, f'✅ Товар "{product.title}" добавлен в корзину!')
            
            return redirect(next_url)
    
    return redirect('catalog')

@login_required
def basket(request):
    basket, created = Basket.objects.get_or_create(user=request.user)
    items = basket.items.all()
    total_price = basket.get_total_price()
    
    return render(request, 'basket.html', {
        'items': items,
        'total_price': total_price,
        'basket_count': basket.get_total_count()
    })

@login_required
def remove_from_basket(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        if item_id:
            basket_item = get_object_or_404(BasketItem, id=int(item_id), basket__user=request.user)
            product_title = basket_item.product.title
            basket_item.delete()
            messages.success(request, f'🗑️ Товар "{product_title}" удален из корзины')
            return redirect('basket')
    return redirect('basket')

@login_required
def update_basket_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        
        basket_item = get_object_or_404(BasketItem, id=int(item_id), basket__user=request.user)
        
        if action == 'increase':
            basket_item.quantity += 1
            basket_item.save()
            messages.success(request, f'✅ Количество увеличено')
        elif action == 'decrease':
            if basket_item.quantity > 1:
                basket_item.quantity -= 1
                basket_item.save()
                messages.success(request, f'✅ Количество уменьшено')
            else:
                product_title = basket_item.product.title
                basket_item.delete()
                messages.success(request, f'🗑️ Товар "{product_title}" удален из корзины')
        
        return redirect('basket')
    return redirect('basket')