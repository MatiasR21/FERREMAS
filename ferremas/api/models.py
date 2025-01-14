from django.db import models

class Producto(models.Model):
    codigo = models.IntegerField(unique=True)
    marca = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

class Carro(models.Model):
    productos = models.ManyToManyField(Producto, through='CarroProducto')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class CarroProducto(models.Model):
    carro = models.ForeignKey(Carro, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    class Meta:
        unique_together = ('carro', 'producto')


class Pedido(models.Model):
    productos = models.ManyToManyField(Producto, related_name='pedidos')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    pagado = models.BooleanField(default=False)  
    metodo_pago = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):
        return f"Pedido {self.id}"
