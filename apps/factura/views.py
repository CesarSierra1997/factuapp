from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.http import Http404,HttpResponse
from django.utils import timezone
from django.contrib import messages
from openpyxl import Workbook
from datetime import datetime
from django.db.models import Q
from ..usuario.mixin import *
from .models import *
from .forms import *


class InicioNegocios(LoginRequiredMixin, ListView):
    model = Negocio
    context_object_name = 'negocios'
    template_name = 'negocios.html'

    def get_queryset(self):
        return Negocio.objects.filter(propietario=self.request.user)

class CrearNegocio(LoginRequiredMixin, CreateView):
    model = Negocio
    form_class = FormNegocio
    template_name = 'crear_negocio.html'
    success_url = reverse_lazy('detalle_negocio')
    pk_url_kwarg = 'negocio_id'


    def form_valid(self, form):
        form.instance.propietario = self.request.user  
        form.instance.fechaCreacion = timezone.now()
        messages.success(self.request, 'Negocio creado correctamente!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('factura:detalle_negocio', kwargs={'negocio_id': self.object.pk})
    
class DetailNegocio(LoginRequiredMixin, DetailView):
    model = Negocio
    template_name = 'detalle_negocio.html'
    pk_url_kwarg = 'negocio_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['facturas'] = Factura.objects.filter(productoServicio__negocio=self.object)
        return context


class EditarNegocio(LoginRequiredMixin, UpdateView):
    model = Negocio
    fields = ['razonSocial', 'nit', 'logo', 'descripcion', 'sitioweb', 'telefono', 'email']
    template_name = 'editar_negocio.html'

    def form_valid(self, form):
        negocio = form.save(commit=False)
        negocio.propietario = self.request.user
        negocio.save()
        return super().form_valid(form)

class EliminarNegocio(LoginRequiredMixin, DeleteView):
    model = Negocio
    template_name = 'eliminar_negocio.html'
    success_url = reverse_lazy('factura:inicio_negocios')

    def get_success_url(self):
        messages.success(self.request, 'Negocio eliminado exitosamente.')
        return super().get_success_url()

    def post(self, request, *args, **kwargs):
        negocio = self.get_object()
        negocio.delete()        
        return super().post(request, *args, **kwargs)

class InicioProductos(LoginRequiredMixin, ListView):
    model = ProductoServicio
    context_object_name = 'productos'
    template_name = 'productos/inicio_productos.html'
    
    def get_queryset(self):
        negocio = Negocio.objects.get(pk=self.kwargs['negocio_id'])
        return ProductoServicio.objects.filter(negocio=negocio)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['negocio'] = Negocio.objects.get(pk=self.kwargs['negocio_id'])
        return context

class CrearProducto(LoginRequiredMixin, CreateView):
    model = ProductoServicio
    form_class = FormProductoServicio
    template_name = 'productos/crear_producto.html'
    success_url = reverse_lazy('factura:inicio_productos')
    
    def form_valid(self, form):
        negocio = Negocio.objects.get(pk=self.kwargs['negocio_id'])
        form.instance.negocio = negocio
        form.instance.fechaCreacion = timezone.now()
        messages.success(self.request, 'Producto agregado correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('factura:inicio_productos', kwargs={'negocio_id': self.object.negocio.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['negocio'] = Negocio.objects.get(pk=self.kwargs['negocio_id'])
        return context

class CrearFactura(LoginRequiredMixin, CreateView):
    model = Factura
    form_class = FormFactura
    template_name = 'factura/crear_factura.html'
    success_url = reverse_lazy('factura:detalle_negocio')

    def get_form_kwargs(self):
        """ Agregar el negocio al formulario para filtrar los productos """
        kwargs = super().get_form_kwargs()
        kwargs['negocio'] = Negocio.objects.get(pk=self.kwargs['negocio_id'])
        return kwargs

    def form_valid(self, form):
        negocio = Negocio.objects.get(pk=self.kwargs['negocio_id'])
        form.instance.negocio = negocio
        messages.success(self.request, 'Factura creada correctamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('factura:detalle_negocio', kwargs={'negocio_id': self.object.negocio.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['negocio'] = Negocio.objects.get(pk=self.kwargs['negocio_id'])  
        return context