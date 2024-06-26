# Generated by Django 3.2.15 on 2024-05-07 16:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0038_order_orderdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='crated_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='создан'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Создан'), ('PAID', 'Оплачен'), ('DONE', 'Выполнен'), ('CANCELLED', 'Отменен')], db_index=True, default='CREATED', max_length=10, verbose_name='статус'),
        ),
        migrations.AddField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='обновлен'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phonenumber',
            field=phonenumber_field.modelfields.PhoneNumberField(db_index=True, max_length=128, region=None, verbose_name='телефон'),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='foodcartapp.order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='foodcartapp.product', verbose_name='Продукт'),
        ),
    ]
