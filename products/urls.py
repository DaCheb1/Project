from django.urls import path
from . import views

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('catalog/<int:pk>/', views.catalog_detail, name='catalog_detail'),
    path('pushbasket/', views.push_basket, name='push_basket'),
    path('basket/', views.basket, name='basket'),
    path('basket/remove/', views.remove_from_basket, name='remove_from_basket'),
]