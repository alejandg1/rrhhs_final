from django.utils import timezone
from django.db import models
from django.forms import model_to_dict
from apps.core.models import ModelBase
from rrhhs.const import CREDIT_INTEREST


class Category(ModelBase):
    Name = models.CharField(verbose_name="nombre", max_length=20)
    description = models.CharField(verbose_name="Descripcion", max_length=100)

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return f'{self.code_item}-{self.name_short}'

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ('-id',)


class Product(ModelBase):
    price = models.FloatField(
        verbose_name='precio', default=0)
    description = models.CharField(verbose_name="Descripcion", max_length=100)
    name = models.CharField(verbose_name="nombre", max_length=20)
    stock = models.IntegerField(verbose_name='stock', default=0)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name='Categoria')

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return self.codigo_rol

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ('id',)


class Client(ModelBase):
    first_name = models.CharField(verbose_name="nombre", max_length=20)
    last_name = models.CharField(verbose_name="apellido", max_length=20)
    email = models.CharField(verbose_name="email", max_length=20)
    phone = models.CharField(verbose_name="telefono", max_length=20)
    address = models.CharField(verbose_name="direccion", max_length=20)

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def getFullName(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ('-id',)


class Cabecera(ModelBase):
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name='Cliente')
    date = models.DateField(verbose_name='Fecha',
                            auto_now_add=True, null=True)
    subtotal = models.FloatField(verbose_name='Subtotal', default=0)
    iva = models.IntegerField(
        verbose_name='Iva', choices=CREDIT_INTEREST,
        default=CREDIT_INTEREST[0][0])
    total = models.FloatField(verbose_name='Total', default=0)

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return f'{self.total}'

    class Meta:
        verbose_name = 'Cabecera factura'
        verbose_name_plural = 'Cabecera facturas'
        ordering = ('-id',)


class Detalle(ModelBase):
    cabecera = models.ForeignKey(
        Cabecera, on_delete=models.CASCADE, verbose_name='Cabecera')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Producto')
    quantity = models.IntegerField(verbose_name='Cantidad', default=0)
    unitprice = models.IntegerField(verbose_name='Precio Unitario', default=0)
    subtotal = models.IntegerField(verbose_name='Subtotal', default=0)

    def get_model_dict(self):
        item = model_to_dict(self)
        return item

    def __str__(self):
        return f'{self.subtotal}'

    class Meta:
        verbose_name = 'Detalle factura'
        verbose_name_plural = 'Detalle Facturas'
        ordering = ('-id',)
