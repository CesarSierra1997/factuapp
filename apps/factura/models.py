from django.db import models
from apps.usuario.models import Usuario

class Negocio(models.Model):
    razonSocial = models.CharField('Nombre', max_length=100, blank=False, null=False)
    nit = models.CharField('NIT', max_length=100, blank=False, null=False)
    logo = models.ImageField('Logo', upload_to='negocio_logo/', max_length=200, blank=True, null=True)
    descripcion = models.CharField('Descripción', max_length=100, blank=False, null=False)
    sitioweb = models.URLField('Sitio web', blank=True, null=True)
    telefono = models.CharField('Teléfono', max_length=100, blank=True, null=True)
    email = models.EmailField('Correo electrónico', max_length=30, unique=True)
    fechaCreacion = models.DateTimeField('Fecha de creación', auto_now_add=True)
    propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return f'{self.razonSocial}'

    class Meta:
        verbose_name_plural = "Negocios"
        ordering = ['id']
        verbose_name = "Negocio"


class ProductoServicio(models.Model):
    nombre = models.CharField('Nombre', max_length=100, blank=False, null=False)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2, blank=False, null=False)
    fechaCreacion = models.DateTimeField('Fecha de creación', auto_now_add=True)
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, blank=False, null=False, related_name='productos')

    def __str__(self):
        return f'{self.nombre} - {self.valor}'


class Factura(models.Model):
    negocio = models.ForeignKey(Negocio, on_delete=models.CASCADE, blank=False, null=False, related_name='facturas')
    fecha = models.DateTimeField('Fecha', auto_now_add=True)
    numeroFactura = models.BigIntegerField('Número de factura', blank=False, null=False, unique=True)

    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('PP', 'Pasaporte'),
        ('RC', 'Registro civil'),
    ]
    tipoDocumento = models.CharField('Tipo de documento', max_length=20, choices=TIPO_DOCUMENTO_CHOICES, default='CC')
    numeroDocumento = models.BigIntegerField('Número de documento', blank=False, null=False)
    nombreCliente = models.CharField('Cliente', max_length=100, blank=False, null=False)
    email = models.EmailField('Correo electrónico', max_length=30)

    total = models.DecimalField('Total', max_digits=10, decimal_places=2, blank=True, null=True)
    pagado = models.BooleanField('Pagado', default=False)

    def calcular_total(self):
        total = sum(detalle.subtotal() for detalle in self.detalles.all())
        self.total = total
        self.save()

    def __str__(self):
        return f'{self.numeroFactura} - {self.nombreCliente} - {self.total} - {self.pagado}'

    class Meta:
        verbose_name_plural = "Facturas"
        ordering = ['numeroFactura']
        verbose_name = "Factura"


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(ProductoServicio, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField('Cantidad', default=1)

    def subtotal(self):
        return self.cantidad * self.producto.valor

    def __str__(self):
        return f'{self.factura.numeroFactura} - {self.producto.nombre} x {self.cantidad}'
