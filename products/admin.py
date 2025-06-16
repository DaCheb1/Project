from django.contrib import admin
from products.models import Category, Product, Manufacturer

admin.site.register(Category)
admin.site.register(Manufacturer)

@admin.register(Product)
class ProductAdmin (admin.ModelAdmin):
    list_display = ['title', 'created_at', 'category__title', 'manufacturer__title']

    def category__title(self, obj):
        return obj.category.title
    
    def manufacturer__title(self, obj):
        return obj.manufacturer.title
    
    category__title.short_description = 'Категория'
    manufacturer__title.short_description = 'Производитель'
