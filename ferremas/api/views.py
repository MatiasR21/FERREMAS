from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import generics, status
from .serializers import ProductoSerializer, CarroSerializer, AgregarProductoCarroSerializer
from rest_framework.response import Response
from .models import Carro, Producto, Pedido, CarroProducto
from rest_framework.views import APIView

class AgregarProductosAlCarro(APIView):
    def post(self, request, format=None):
        carro, created = Carro.objects.get_or_create(id=1)
        serializer = AgregarProductoCarroSerializer(data=request.data)
        if serializer.is_valid():
            codigo = serializer.validated_data['codigo']
            cantidad = serializer.validated_data['cantidad']
            try:
                producto = Producto.objects.get(codigo=codigo)
            except Producto.DoesNotExist:
                return Response({"error": f"Producto con código {codigo} no existe."}, status=status.HTTP_404_NOT_FOUND)
            
            carro_producto, created = CarroProducto.objects.get_or_create(carro=carro, producto=producto, defaults={'cantidad': cantidad})
            if created:
                carro_producto.cantidad = cantidad
            else:
                carro_producto.cantidad += cantidad
            carro_producto.save()
            
            return Response({"mensaje": f"Producto '{producto.nombre}' agregado correctamente al carro."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CarroDetail(APIView):
    def get(self, request, format=None):
        try:
            carro = Carro.objects.get(id=1)
        except Carro.DoesNotExist:
            return Response({"error": "El carro no existe."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CarroSerializer(carro)
        total = sum(item['precio'] * item['cantidad'] for item in serializer.data['productos'])
        response_data = {
            'productos': serializer.data['productos'],
            'total': total
        }
        return Response(response_data, status=status.HTTP_200_OK)

class ProductoListCreate(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class ProductoRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    lookup_field = 'codigo'

from django.http import JsonResponse

def eliminar_producto(request, codigo):
    try:
        producto = Producto.objects.get(codigo=codigo)
    except Producto.DoesNotExist:
        return JsonResponse({"mensaje": "El producto no existe."}, status=status.HTTP_404_NOT_FOUND)
    producto.delete()
    return JsonResponse({"mensaje": "El producto ha sido eliminado correctamente."}, status=status.HTTP_200_OK)

class EliminarProductoDelCarro(APIView):
    def delete(self, request, producto_codigo, format=None):
        try:
            producto = Producto.objects.get(codigo=producto_codigo)
        except Producto.DoesNotExist:
            return Response({"error": f"Producto con código {producto_codigo} no existe."}, status=status.HTTP_404_NOT_FOUND)

        try:
            carro = Carro.objects.get(id=1)
        except Carro.DoesNotExist:
            return Response({"error": "El carro no existe."}, status=status.HTTP_404_NOT_FOUND)

        if producto in carro.productos.all():
            carro.productos.remove(producto)
            return Response({"mensaje": f"Producto '{producto.nombre}' eliminado correctamente del carro."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"Producto '{producto.nombre}' no está en el carro."}, status=status.HTTP_400_BAD_REQUEST)


class PagarYFinalizarCarro(APIView):
    def post(self, request, format=None):
        try:
            carro = Carro.objects.get(id=1)
        except Carro.DoesNotExist:
            return Response({"error": "Carro no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        metodo_pago = request.data.get('metodo_pago', None)
        if not metodo_pago:
            return Response({"error": "Método de pago no proporcionado."}, status=status.HTTP_400_BAD_REQUEST)
        
        total = sum(item.producto.precio * item.cantidad for item in carro.carroproducto_set.all())
        pedido = Pedido.objects.create(total=total, pagado=True, metodo_pago=metodo_pago)
        productos_nombres = []
        for carro_producto in carro.carroproducto_set.all():
            producto = carro_producto.producto
            cantidad_comprada = carro_producto.cantidad
            if producto.stock < cantidad_comprada:
                return Response({"error": f"Stock insuficiente para el producto '{producto.nombre}'."}, status=status.HTTP_400_BAD_REQUEST)
            producto.stock -= cantidad_comprada
            producto.save()
            pedido.productos.add(producto)
            productos_nombres.append({
                "nombre": producto.nombre,
                "precio": producto.precio,
                "cantidad": cantidad_comprada
            })
        carro.carroproducto_set.all().delete()
        carro.delete()
        return Response({
            "mensaje": "Carro pagado y pedido finalizado correctamente.",
            "total": total,
            "metodo_pago": metodo_pago,
            "productos": productos_nombres
        }, status=status.HTTP_200_OK)
