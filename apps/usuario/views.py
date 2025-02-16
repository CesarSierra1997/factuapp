import json
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from ..usuario.forms import FormularioLogin
from django.urls import reverse_lazy
from django.utils.decorators import  method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView
from apps.usuario.models import Usuario
from apps.usuario.forms import *
from apps.usuario.mixin import *

class Inicio(TemplateView): #vista basada en clases para una sola vista
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class Login(FormView):
    template_name = "login.html"
    form_class = FormularioLogin
    success_url = reverse_lazy('factura:inicio_negocios')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)

    #redefinir método dispatch() 
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            usuario = request.user
            print(f"*************El usuario id: {usuario.id} - nombre: {usuario}, ya Inicio Sesión****************")
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        login(self.request,form.get_user())
        return super(Login,self).form_valid(form)
    
def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/')


class InicioUsuario(LoginSuperStaffMixin, ValidarPermisosMixin, TemplateView):
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')
    template_name = 'usuario/listar_usuarios.html'

class Registro(TemplateView):
    model = Usuario
    template_name = 'usuario/registro.html'
        
class RegistrarUsuario(CreateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = "usuario/registrar_usuario.html"

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX
            form = self.form_class(request.POST)
            if form.is_valid():
                usuario = form.save(commit=False)  # Guarda el usuario sin confirmar aún
                usuario.set_password(form.cleaned_data['password1'])  # Encripta la contraseña
                usuario.save()  # Guarda el usuario en la base de datos

                mensaje = f"{self.model.__name__} registrado correctamente!"
                return JsonResponse({'mensaje': mensaje, 'error': None}, status=201)
            else:
                return JsonResponse({'mensaje': "Error al registrar usuario", 'error': form.errors}, status=400)
        else:
            return redirect('usuario:registro')

class EditarUsuario(LoginSuperStaffMixin, ValidarPermisosMixin, UpdateView):
    model = Usuario
    form_class = FormularioUsuario
    template_name = "usuario/editar_usuario.html"
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')


    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form = self.form_class(request.POST, instance = self.get_object())
            if form.is_valid():
                form.save()
                mensaje = f'¡{self.model.__name__} actualizado correctamente!'
                error = f'no hay error'
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 201
                return response
            else:
                mensaje = f'{self.model.__name__} no se ha podido actualizar'
                error = form.errors
                response = JsonResponse({'mensaje':mensaje, 'error':error})
                response.status_code = 400
                return response
        else:
            return redirect('usuario:inicio_usuarios')
        
class EliminarUsuario(LoginSuperStaffMixin, ValidarPermisosMixin, DeleteView):
    model = Usuario
    template_name = "usuario/eliminar_usuario.html"
    success_url = reverse_lazy('usuario:inicio_usuarios')
    permission_required = ('usuario.view_usuario', 'usuario.add_usuario', 'usuario.delete_usuario', 'usuario.change_usuario')


    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            usuario = self.get_object()
            usuario.is_active = False
            usuario.save()
            mensaje = f'¡{self.model.__name__} eliminado correctamente!'
            error = f'no hay error'
            response = JsonResponse({'mensaje':mensaje, 'error':error})
            response.status_code = 201
            return response
        else:
            return redirect('usuario:inicio_usuarios')

        
