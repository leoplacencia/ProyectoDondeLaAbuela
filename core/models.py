from django.db import models

# Create your models here.
class Venta(models.Model):
    id_pedido = models.IntegerField(verbose_name="Pedido")
    estado = models.IntegerField(verbose_name="Estado", default=1)
    created = models.DateTimeField(auto_now_add=True, verbose_name = "Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name = "Fecha de modificación")

    class Meta:
        verbose_name = "venta"
        verbose_name_plural = "ventas"
        ordering = ['-created']
    def __str__(self):
        return "%s" % self.id_pedido