from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required


app_name = 'factura'  

urlpatterns = [

    path('negocios/', InicioNegocios.as_view(), name='inicio_negocios'),
    path('crear_negocio/', CrearNegocio.as_view(), name='crear_negocio'),
    path('detalle_negocio/<int:negocio_id>/', DetailNegocio.as_view(), name='detalle_negocio'),
    path('editar_negocio/<int:pk>/', EditarNegocio.as_view(), name='editar_negocio'),
    path('eliminar_negocio/<int:pk>/', EliminarNegocio.as_view(), name='eliminar_negocio'),

    path('detalle_negocio/<int:negocio_id>/productos/', InicioProductos.as_view(), name='inicio_productos'),
    path('detalle_negocio/<int:negocio_id>/crear_producto/', CrearProducto.as_view(), name='crear_producto'),

    path('detalle_negocio/<int:negocio_id>/crear_factura/', CrearFactura.as_view(), name='crear_factura'),
    # path('detalle_factura/<int:pk>/', DetailFactura.as_view(), name='detalle_factura'),
    # path('editar_factura/<int:pk>/', EditarFactura.as_view(), name='editar_factura'),
    # path('eliminar_factura/<int:pk>/', EliminarFactura.as_view(), name='eliminar_factura'),


]
