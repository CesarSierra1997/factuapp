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
        fields = ['numeroFactura', 'tipoDocumento', 'numeroDocumento', 'nombreCliente', 'email', 'productoServicio', 'pagado','total']
        widgets = {
            'numeroFactura': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Número de factura',
                    'required':'required'
                }
            ),
            'tipoDocumento': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Seleccione el tipo de documento'
                }),
            'numeroDocumento': forms.NumberInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Ingrese el numero de documento'
                }),
            'nombreCliente': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Ingrese el nombre del cliente',
                    'required':'required'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Correo electrónico'
                }
            ),
            'productoServicio': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Seleccione el producto o servicio'
                }),
            'pagado': forms.CheckboxInput(
                attrs={
                    'placeholder':'Ingrese si el cliente ha pagado la factura',
                }),
        }

    def __init__(self, *args, **kwargs):
        negocio = kwargs.pop('negocio', None)  # Obtener el negocio pasado desde la vista
        super().__init__(*args, **kwargs)
        if negocio:
            self.fields['productoServicio'].queryset = ProductoServicio.objects.filter(negocio=negocio)

