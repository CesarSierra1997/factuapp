#Importarmos libreria para las urls
from django.urls import path
from .views import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    #Vsitas bassadas en funciones <int:id>
    #Vsitas bassadas en clases <int:pk>
    path('inicio_usuarios/', InicioUsuario.as_view(), name='inicio_usuarios'),
    path('registro/', Registro.as_view(), {'parametro_extra': 'parametro extra ej'}, name='registro'),
    path('registrar_usuario/', RegistrarUsuario.as_view(), name='registrar_usuario'),
    path('editar_usuario/<int:pk>/', EditarUsuario.as_view(), name='editar_usuario'),
    path('eliminar_usuario/<int:pk>/', EliminarUsuario.as_view(), name='eliminar_usuario'),

]  

# URLS DE VISTAS IMPLICITAS
# urlpatterns += [
#     path('inicio_usuarios/', login_required(
#                                 TemplateView.as_view(
#                                     template_name='usuario/listar_usuarios.html'
#                                 )), name='inicio_usuarios'),
# ]  