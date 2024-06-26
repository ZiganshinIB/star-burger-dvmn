from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.utils.translation import gettext_lazy
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class OrderQuerySet(models.QuerySet):
    def active(self):
        return self.filter(status=1)


class Order(models.Model):

    OrderStatus = [
            ('1', 'Необработан'),
            ('2', 'В обработке'),
            ('3', 'Готов к выдаче'),
            ('4', 'Выполнен'),
            ('5', 'Отменен'),
        ]
    PaymentMethod = [
        ('NONE', "Не выбрано"),
        ('CASH', 'Наличные'),
        ('CARD', 'Карта'),
        ('ELECT', 'Электронно'),

    ]

    firstname = models.CharField(
        verbose_name='имя',
        max_length=50,
    )
    lastname = models.CharField(
        verbose_name='фамилия',
        max_length=50,
    )
    phonenumber = PhoneNumberField(
        verbose_name='телефон',
        region='RU',
        db_index=True,
    )
    address = models.CharField(
        verbose_name='адрес',
        max_length=100,
    )
    comment = models.TextField(
        verbose_name='Комментарий',
        blank=True,
    )
    status = models.CharField(
        verbose_name='статус',
        choices=OrderStatus,
        db_index=True,
        default=1,
        max_length=1,
    )
    payment_method = models.CharField(
        verbose_name='Способ оплаты',
        choices=PaymentMethod,
        max_length=10,
        default='NONE',
    )

    registered_at = models.DateTimeField(
        verbose_name='Cоздан',
        auto_now_add=True,
    )
    called_at = models.DateTimeField(
        verbose_name='Дата звонка',
        null=True,
        blank=True
    )
    delivered_at = models.DateTimeField(
        verbose_name='Дата доставки',
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        verbose_name='обновлен',
        auto_now=True,
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='ресторан',
        related_name='orders',
        null=True,
        on_delete=models.SET_NULL
    )
    total_price = models.DecimalField(
        verbose_name='Стоимость заказа',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    objects = OrderQuerySet.as_manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ['status', '-registered_at']

    def get_total_price(self):
        return self.objects.annotate(total_price_=Sum("products__product__price")).get(id=self.id).total_price_

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class OrderDetails(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Заказ',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Продукт',
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[MinValueValidator(1)]
    )

    def get_price(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = 'позиция заказа'
        verbose_name_plural = 'позиции заказа'
