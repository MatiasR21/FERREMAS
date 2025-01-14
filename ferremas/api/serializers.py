from rest_framework import serializers
from .models import Producto, Carro, Pedido, CarroProducto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['codigo', 'marca', 'nombre', 'precio', 'stock']

class ProductoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['codigo', 'nombre', 'precio']

class CarroProductoSerializer(serializers.ModelSerializer):
    codigo = serializers.ReadOnlyField(source='producto.codigo')
    nombre = serializers.ReadOnlyField(source='producto.nombre')
    precio = serializers.ReadOnlyField(source='producto.precio')

    class Meta:
        model = CarroProducto
        fields = ['codigo', 'nombre', 'precio', 'cantidad']

class CarroSerializer(serializers.ModelSerializer):
    productos = CarroProductoSerializer(source='carroproducto_set', many=True)
    class Meta:
        model = Carro
        fields = ['id', 'productos', 'fecha_creacion']

class AgregarProductoCarroSerializer(serializers.Serializer):
    codigo = serializers.IntegerField()
    cantidad = serializers.IntegerField()

class PedidoSerializer(serializers.ModelSerializer):
    productos = ProductoSerializer(many=True)
    class Meta:
        model = Pedido
        fields = ('id', 'fecha_creacion', 'productos', 'total', 'pagado', 'metodo_pago')  # Incluir método de pago
