from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from products.models import Product, Category, Basket
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

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
        'products_count': products.count(),  # ← ЭТО ВАЖНО! Добавлена эта строка
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
        if product_id:
            product = get_object_or_404(Product, id=int(product_id))
            basket, created = Basket.objects.get_or_create(user=request.user)
            basket.products.add(product)
            messages.success(request, f'✅ Товар "{product.title}" добавлен в корзину!')
            return redirect('catalog')
    return redirect('catalog')

@login_required
def basket(request):
    basket, created = Basket.objects.get_or_create(user=request.user)
    products = basket.products.all()
    total_price = sum(product.price for product in products)
    
    return render(request, 'basket.html', {
        'products': products,
        'total_price': total_price,
        'basket_count': products.count()
    })

@login_required
def remove_from_basket(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            product = get_object_or_404(Product, id=int(product_id))
            basket = Basket.objects.get(user=request.user)
            basket.products.remove(product)
            messages.success(request, f'🗑️ Товар "{product.title}" удален из корзины')
            return redirect('basket')
    return redirect('basket')

def index(request):
    # Получаем популярные товары для главной страницы
    popular_products = Product.objects.all()[:8]
    
    # Получаем категории для быстрого доступа
    categories = Category.objects.all()[:6]
    
    return render(request, 'index.html', {
        'popular_products': popular_products,
        'categories': categories
    })

# ========== АУТЕНТИФИКАЦИЯ ==========

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '🎉 Регистрация прошла успешно! Добро пожаловать!')
            return redirect('catalog')
        else:
            messages.error(request, '⚠️ Пожалуйста, исправьте ошибки в форме')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'👋 Добро пожаловать, {username}!')
                return redirect('catalog')
        else:
            messages.error(request, '❌ Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, '👋 Вы успешно вышли из системы')
    return redirect('catalog')

@login_required
def account(request):
    # Получаем историю заказов (если будете добавлять заказы)
    user_basket = Basket.objects.get(user=request.user)
    recent_products = user_basket.products.all()[:5]
    
    return render(request, 'account.html', {
        'user': request.user,
        'recent_products': recent_products,
        'basket_count': user_basket.products.count()
    })