from django.urls import path
from .views import ProductoListCreate, ProductoRetrieveUpdateDestroy, eliminar_producto, AgregarProductosAlCarro, CarroDetail,EliminarProductoDelCarro, PagarYFinalizarCarro

urlpatterns = [
    path('productos/', ProductoListCreate.as_view(), name='producto-list-create'),
    path('productos/<str:codigo>/', ProductoRetrieveUpdateDestroy.as_view(), name='producto-detail'),  
    path('eliminar-producto/<str:codigo>/', eliminar_producto, name='eliminar-producto'),  
    path('carro/productos/', AgregarProductosAlCarro.as_view(), name='agregar-productos-carro'),
    path('carro/detalle/', CarroDetail.as_view(), name='carro-detalle'),
    path('carro/productos/<int:producto_codigo>/', EliminarProductoDelCarro.as_view(), name='eliminar-producto-carro'),
    path('carro/finalizar/', PagarYFinalizarCarro.as_view(), name='pagar-y-finalizar-carro'),
]
