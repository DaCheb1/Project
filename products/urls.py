from django.urls import path
from products.views import catalog, catalog_detail, push_basket, basket
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # Маршруты для товаров
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:pk>/', catalog_detail, name='catalog_detail'),
    path('pushbasket/', push_basket, name='push_basket'),
    path('basket/', basket, name='basket'),
    path('basket/remove/', views.remove_from_basket, name='remove_from_basket'),
    
    # ========== НОВЫЕ МАРШРУТЫ ДЛЯ АУТЕНТИФИКАЦИИ ==========
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account, name='account'),
]