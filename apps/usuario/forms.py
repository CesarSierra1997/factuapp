from typing import Any
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario
from django import forms
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re

class FormularioLogin(AuthenticationForm):    
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder']='Nombre de usuario'
        self.fields['username'].widget.attrs['id'] = 'username-mejorado'
        self.fields['password'].widget.attrs['class']='form-control'
        self.fields['password'].widget.attrs['placeholder']='Contraseña'

class FormularioUsuario(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget = forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Ingrese su Contraseña',
            'id':'password1',
            'required':'required'
        }
    ))
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput(
        attrs={
            'class':'form-control',
            'placeholder':'Confirme la contraseña ingresada',
            'id':'password2',
            'required':'required'
        }
    ))
    class Meta:
        model = Usuario
        fields = ['tipoDocumento','numeroDocumento','nombres', 'apellidos','email','username' ]
        widgets = {
            'tipoDocumento': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Seleccione el tipo de documento'
                }),
            'numeroDocumento': forms.NumberInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Ingrese el numero de documento'
                }),
            'email': forms.EmailInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Correo electrónico'
                }
            ),
            'nombres': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Digite su nombre',
                    'required':'required'
                }
            ),
            'apellidos': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Digite sus apellidos',
                    'required':'required'
                }
            ),
            'username': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Nombre de usuario - caracteres permitidos ( /, *, +, -, ., _ )'
                }
            ),
        }
    def clean_numeroDocumento(self):
        numeroDoc = self.cleaned_data["numeroDocumento"]
        numeroDoc_str = str(numeroDoc)
        if len(str(numeroDoc_str)) < 10:
            raise ValidationError(_('El número de documento debe tener al menos 10 caracteres.'))
        if not numeroDoc_str.isdigit():
            raise ValidationError(_('El número de documento debe ser un número entero.'))
        return numeroDoc
    

    def clean_nombres(self):
        nombres = self.cleaned_data.get('nombres')
        if not nombres:
            raise ValidationError(_('Este campo es obligatorio.'))
        if not nombres.replace(" ", "").isalpha():
            raise ValidationError(_('El nombre solo debe contener letras.'))
        return nombres.lower()   

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not apellidos:
            raise ValidationError(_('Este campo es obligatorio.'))
        if not apellidos.replace(" ", "").isalpha():
            raise ValidationError(_('Los apellidos solo deben contener letras.'))
        return apellidos.lower()    

    def clean_username(self):
            username = self.cleaned_data.get('username')
            username = username.replace(" ", "_")
            # Longitud mínima de 4 caracteres
            if len(username) < 4:
                raise ValidationError(_('El nombre de usuario debe tener al menos 4 caracteres.'))

            # Validar que contenga al menos una letra
            if not re.search(r'[a-zA-Z]', username):
                raise ValidationError(_('El nombre de usuario debe contener al menos una letra.'))

            caracteres_permitidos = set("/-*+._1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
            if not all(char in caracteres_permitidos for char in username):
                raise ValidationError(_('Se permiten solo caracteres alfanuméricos y los siguientes especiales: /, *, -, +, ., _'))
            return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Las contraseñas no coinciden')

            # Usar la función de validación de Django para contraseñas seguras
            try:
                validate_password(password2)
            except ValidationError as e:
                raise forms.ValidationError(e)

            # Validar longitud mínima de 8 caracteres
            if len(password2) < 8:
                raise ValidationError(_('La contraseña debe tener al menos 8 caracteres.'))

            # Validar que contenga al menos una mayúscula, una minúscula, un número y un carácter especial
            if not re.search(r'[A-Z]', password2):
                raise ValidationError(_('La contraseña debe contener al menos una letra mayúscula.'))
            if not re.search(r'[a-z]', password2):
                raise ValidationError(_('La contraseña debe contener al menos una letra minúscula.'))
            if not re.search(r'\d', password2):
                raise ValidationError(_('La contraseña debe contener al menos un número.'))
            if not re.search(r'[/*\-+._]', password2):
                raise ValidationError(_('La contraseña debe contener al menos un carácter especial: /, *, -, +, ., _'))

        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
# Formulario para actualizar ciertos datos de un usuario registrado PERFIL: correo, contraseña
# class FormularioUpdateUsuario(forms.ModelForm):
#     class Meta:
#         model = Usuario
#         fields = ['nombres', 'apellidos','email' ]
#         widgets = {

#             'email': forms.EmailInput(
#                 attrs={
#                     'class':'form-control',
#                     'placeholder':'Correo electrónico'
#                 }
#             ),
#             'nombres': forms.TextInput(
#                 attrs={
#                     'class':'form-control',
#                     'placeholder':'Digite su nombre',
#                     'required':'required'
#                 }
#             ),
#             'apellidos': forms.TextInput(
#                 attrs={
#                     'class':'form-control',
#                     'placeholder':'Digite sus apellidos',
#                     'required':'required'
#                 }
#             ),
#         }

