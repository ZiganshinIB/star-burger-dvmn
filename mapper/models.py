from django.db import models
# Create your models here.

class Address(models.Model):
    address = models.CharField(max_length=256, unique=True, verbose_name='адрес', db_index=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)


    def __str__(self):
        return self.address
