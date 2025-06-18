from django.contrib import admin
from products.models import Category, Product, Manufacturer
from django.db.models import JSONField
from django_json_widget.widgets import JSONEditorWidget
admin.site.register(Category)
admin.site.register(Manufacturer)

@admin.register(Product)
class ProductAdmin (admin.ModelAdmin):
    list_display = ['title', 'created_at', 'category__title', 'manufacturer__title']
    formfield_overrides = {JSONField: {'widget': JSONEditorWidget }}

    def category__title(self, obj):
        return obj.category.title
    
    def manufacturer__title(self, obj):
        return obj.manufacturer.title
    
    category__title.short_description = 'Категория'
    manufacturer__title.short_description = 'Производитель'
