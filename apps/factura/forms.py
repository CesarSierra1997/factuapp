from django.forms import inlineformset_factory
from django import forms
from .models import *

class FormNegocio(forms.ModelForm):
    class Meta:
        model = Negocio
        fields = ['razonSocial', 'nit', 'logo', 'descripcion', 'sitioweb', 'telefono', 'email']
        widgets = {
            'razonSocial': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese el nombre de la empresa',
                    'required':'required'
                }
            ),
            'logo': forms.FileInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese la imagen de la empresa',
                    'required':'required'
                }
            ),
            'nit': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese el NIT de la empresa',
                    'required':'required'
                }
            ),
            'descripcion': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese la descripción de la empresa',
                    'required':'required'
                }
            ),
            'sitioweb': forms.URLInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese el sitio web de la empresa',
                    'required':'required'
                }
            ),
            'telefono': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese el teléfono de la empresa',
                    'required':'required'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Correo electrónico'
                }
            ),
        }

class FormProductoServicio(forms.ModelForm):
    class Meta:
        model = ProductoServicio
        fields = ['nombre', 'valor']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese el nombre del producto o servicio',
                    'required':'required'
                }
            ),
            'valor': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese el valor',
                    'required':'required'
                }
            ),
        }

class FormFactura(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['numeroFactura', 'tipoDocumento', 'numeroDocumento', 'nombreCliente', 'email', 'pagado']

        widgets = {
            'numeroFactura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de factura'}),
            'tipoDocumento': forms.Select(attrs={'class': 'form-control'}),
            'numeroDocumento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Número de documento'}),
            'nombreCliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'pagado': forms.CheckboxInput(),
        }


from django.forms import BaseModelFormSet

class FormDetalleFactura(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = ['producto', 'cantidad']

        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        negocio_id = kwargs.pop('negocio_id', None)  # Extraer el negocio antes de llamar a super()
        super().__init__(*args, **kwargs)
        if negocio_id:
            self.fields['producto'].queryset = ProductoServicio.objects.filter(negocio_id=negocio_id)

class BaseDetalleFacturaFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.negocio_id = kwargs.pop('negocio_id', None)  # Extraer negocio antes de llamar a super()
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.negocio_id = self.negocio_id  # Pasar negocio_id a cada formulario dentro del formset

# DetalleFacturaFormSet = forms.modelformset_factory(
#     DetalleFactura,
#     form=FormDetalleFactura,
#     formset=BaseDetalleFacturaFormSet,
#     extra=1
# )
