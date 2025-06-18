from django.urls import path
from products.views import catalog
urlpatterns = [
    path('catalog/', catalog, name = 'catalog')
]