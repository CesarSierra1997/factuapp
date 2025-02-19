from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView, FormView
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.http import Http404,HttpResponse, HttpResponseRedirect
import json
import qrcode
import qrcode.image.pil
from django.utils.html import escape
from io import BytesIO
from xhtml2pdf import pisa
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
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
        context['facturas'] = Factura.objects.filter(negocio=self.object)
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

class CrearFactura(CreateView):
    model = Factura
    form_class = FormFactura
    template_name = "factura/crear_factura.html"

    def form_valid(self, form):
        # Guardamos la Factura
        self.object = form.save(commit=False)
        negocio_id = self.kwargs.get("negocio_id")
        negocio = get_object_or_404(Negocio, id=negocio_id)
        self.object.negocio = negocio
        self.object.save()

        # Obtenemos el JSON de detalles
        detalles_json = self.request.POST.get("detalles_json", "[]")
        try:
            detalles = json.loads(detalles_json)
        except json.JSONDecodeError:
            detalles = []

        # Creamos cada DetalleFactura
        for detalle in detalles:
            producto_id = detalle.get("producto_id")
            cantidad = detalle.get("cantidad", 1)
            
            # Obtenemos el producto (ProductoServicio)
            producto = get_object_or_404(ProductoServicio, id=producto_id)
            
            # Crea el detalle solo con los campos que existen en el modelo
            DetalleFactura.objects.create(
                factura=self.object,
                producto=producto,
                cantidad=cantidad,
            )
        self.object.calcular_total()

        # Generar el código QR con la URL pública de la factura
        factura_url = f"https://factuapp.onrender.com{reverse('factura:ver_factura', kwargs={'factura_id': self.object.id})}"
        qr = qrcode.make(factura_url, image_factory=qrcode.image.pil.PilImage)

        # Convertir QR a Base64
        qr_io = BytesIO()
        qr.save(qr_io, format='PNG')
        qr_base64 = base64.b64encode(qr_io.getvalue()).decode('utf-8')

        # Guardar QR en Base64 en la base de datos
        self.object.qrCode = qr_base64
        self.object.save()

        # Redirigimos normalmente
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        negocio_id = self.kwargs.get('negocio_id')
        negocio = get_object_or_404(Negocio, id=negocio_id)
        context['negocio'] = negocio
        # Listamos productos de este negocio
        context['productos'] = ProductoServicio.objects.filter(negocio=negocio)
        return context

    def get_success_url(self):
        return reverse_lazy("factura:detalle_negocio", kwargs={"negocio_id": self.object.negocio.id})
    
class VerFactura(DetailView):
    model = Factura
    template_name = 'factura/ver_factura.html'
    pk_url_kwarg = 'factura_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['factura'] = self.object
        return context


def generar_pdf(request, factura_id):
    # Obtener la factura
    factura = get_object_or_404(Factura, id=factura_id)

    # Obtener la URL absoluta de la imagen del logo
    logo_url = request.build_absolute_uri(factura.negocio.logo.url) if factura.negocio.logo else None

    # Renderizar el template con los datos de la factura y la imagen del logo
    html_content = render_to_string('factura/pdf_template.html', {'factura': factura, 'logo_url': logo_url})

    # Crear un objeto BytesIO para almacenar el PDF
    pdf_buffer = BytesIO()

    # Convertir HTML a PDF
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_buffer)

    # Si hay errores al generar el PDF
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)

    # Responder con el PDF generado
    pdf_buffer.seek(0)
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=factura_{factura.numeroFactura}.pdf'

    return response
