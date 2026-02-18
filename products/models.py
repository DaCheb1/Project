from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum

class Category(models.Model):
    title = models.CharField('Название', max_length=60)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

class Manufacturer(models.Model):
    title = models.CharField('Название', max_length=30)
    logo = models.ImageField('Логотип', upload_to='manufacturer/', blank=True, null=True)
    categories = models.ManyToManyField(Category, verbose_name='Категория', related_name='manufacturers')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
        ordering = ['title']
    
class Product(models.Model):
    title = models.CharField("Название", max_length=100)
    desc = models.TextField("Описание", blank=True, null=True)
    price = models.IntegerField("Цена", default=0)
    image = models.ImageField("Изображение", upload_to='products/', blank=True, null=True)
    country = models.CharField('Страна производитель', max_length=30)
    chars = models.JSONField('Характеристики', blank=True, null=True)
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, verbose_name='Производитель', related_name='products', on_delete=models.CASCADE)
    created_at = models.DateField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']

class BasketItem(models.Model):
    """Модель для товара в корзине с количеством"""
    basket = models.ForeignKey('Basket', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='basket_items')
    quantity = models.PositiveIntegerField('Количество', default=1)
    added_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        unique_together = ['basket', 'product']
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
    
    def get_total_price(self):
        """Общая стоимость для этой позиции"""
        return self.product.price * self.quantity

class Basket(models.Model):
    user = models.OneToOneField(User, verbose_name='Владелец корзины', related_name='basket', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    def __str__(self):
        return f"Корзина {self.user.username}"
    
    def get_total_price(self):
        """Общая стоимость всех товаров в корзине"""
        return sum(item.get_total_price() for item in self.items.all())
    
    def get_total_count(self):
        """Общее количество товаров в корзине"""
        return self.items.aggregate(total=Sum('quantity'))['total'] or 0
    
    def get_items(self):
        """Получение всех товаров в корзине"""
        return self.items.all()
    
    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

@receiver(post_save, sender=User)
def create_user_basket(sender, instance, created, **kwargs):
    """Создание корзины при регистрации пользователя"""
    if created:
        Basket.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_basket(sender, instance, **kwargs):
    """Сохранение корзины при сохранении пользователя"""
    if hasattr(instance, 'basket'):
        instance.basket.save()