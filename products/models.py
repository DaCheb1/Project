from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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

class Basket(models.Model):
    user = models.OneToOneField(User, verbose_name='Владелец корзины', related_name='basket', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, verbose_name='Товары', related_name='baskets')
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

@receiver(post_save, sender=User)
def create_user_basket(sender, instance, created, **kwargs):
    if created:
        Basket.objects.create(user=instance)
@receiver(post_save,sender=User)
def save_user_basket(sender, instance, **kwargs):
    instance.basket.save()