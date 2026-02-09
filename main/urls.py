from django.urls import path
from products.views import catalog, catalog_detail, push_basket, basket, remove_from_basket
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', catalog, name='catalog'),
    path('catalog/<int:pk>/', catalog_detail, name='catalog_detail'),
    path('pushbasket/', push_basket, name='push_basket'),
    path('basket/', basket, name='basket'),
    path('basket/remove/', remove_from_basket, name='remove_from_basket'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account, name='account'),
]