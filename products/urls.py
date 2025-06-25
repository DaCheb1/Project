from django.urls import path
from products.views import catalog, catalog_detail, push_basket, basket
urlpatterns = [
    path('catalog/', catalog, name = 'catalog'), 
    path('catalog/<int:pk>/', catalog_detail, name = 'catalog_detail'),
    path('pushbasket/',push_basket, name = 'push_basket'),
    path('basket/', basket, name = 'basket')
]