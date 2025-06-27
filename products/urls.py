from django.urls import path
from products.views import catalog, catalog_detail, push_basket, basket
from . import views
urlpatterns = [
    path('catalog/', catalog, name = 'catalog'), 
    path('catalog/<int:pk>/', catalog_detail, name = 'catalog_detail'),
    path('pushbasket/',push_basket, name = 'push_basket'),
    path('basket/', basket, name = 'basket'),
    path('basket/remove/', views.remove_from_basket, name='remove_from_basket'),
    path('', views.index, name='index'),  # Добавьте эту строку
    path('catalog/', views.catalog, name='catalog'),
]