from django.urls import path
from products.views import catalog, catalog_detail
urlpatterns = [
    path('catalog/', catalog, name = 'catalog'), 
    path('catalog/<int:pk>/', catalog_detail, name = 'catalog_detail')
]