from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Category, Basket
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

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
            messages.success(request, f'Товар "{product.title}" добавлен в корзину!')
            return redirect('catalog')
    return redirect('catalog')

@login_required
def basket(request):
    basket, created = Basket.objects.get_or_create(user=request.user)
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
            messages.success(request, f'Товар "{product.title}" удален из корзины')
            return redirect('basket')
    return redirect('basket')

def index(request):
    return render(request, 'index.html')

# ========== НОВЫЕ ФУНКЦИИ ДЛЯ АУТЕНТИФИКАЦИИ ==========

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            messages.success(request, 'Регистрация прошла успешно! Добро пожаловать!')
            return redirect('catalog')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
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
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('catalog')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('catalog')

@login_required
def account(request):
    return render(request, 'account.html', {'user': request.user})
