from django.db import models

class Category (models.Model):
    title = models.CharField('Название', max_length=60)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Manufacturer (models.Model):
    title = models.CharField('Название', max_length=30)
    logo = models.ImageField('Логотип', upload_to='manufacturer/')
    categories = models.ManyToManyField(Category, verbose_name='Категория', related_name='manufacturers')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
    
class Product (models.Model):
    title = models.CharField("", max_length=100)
    desc = models.TextField("Описание", blank=True, null=True)
    price = models.IntegerField("Цена", default=0)
    image = models.ImageField("Изображение", upload_to='products/', blank=True, null=True)
    country = models.CharField('Страна производитель', max_length=30)
    chars = models.JSONField('Характеристики', blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Проиводитель', related_name='products', on_delete=models.CASCADE)
    created_at = models.DateField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

