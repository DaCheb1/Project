from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Basket, Product, Category
from django.db.models import Count

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'🎉 Регистрация прошла успешно! Добро пожаловать, {user.username}!')
            return redirect('catalog')
        else:
            # Собираем все ошибки формы
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'⚠️ {error}')
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
                messages.success(request, f'👋 С возвращением, {username}!')
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
    # Получаем корзину пользователя
    basket, created = Basket.objects.get_or_create(user=request.user)
    
    # Статистика корзины
    basket_count = basket.get_total_count()
    basket_total = basket.get_total_price()
    
    # Получаем товары для отображения (последние 5)
    recent_items = basket.items.order_by('-added_at')[:5]
    
    # Получаем все категории для отображения
    categories = Category.objects.annotate(
        product_count=Count('products')
    ).filter(product_count__gt=0)[:6]
    
    # Рекомендуемые товары
    recommended_products = Product.objects.order_by('-created_at')[:4]
    
    return render(request, 'account.html', {
        'user': request.user,
        'basket_count': basket_count,
        'basket_total': basket_total,
        'recent_items': recent_items,
        'categories': categories,
        'recommended_products': recommended_products,
        'date_joined': request.user.date_joined,
        'last_login': request.user.last_login,
    })