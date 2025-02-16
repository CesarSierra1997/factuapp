from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

class LoginSuperStaffMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff and request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else: 
                messages.error(request, 'No tienes permisos para acceder a esta vista.')
        else: 
            messages.warning(request, 'Debe iniciar sesión para acceder a esta sección.')
        return redirect('index')

class ValidarPermisosMixin(object):
    permission_required = ''
    url_redirect = None

    def get_perms(self):
        if isinstance(self.permission_required,str): return (self.permission_required)
        else: return self.permission_required 

    def get_url_redirect(self):
        if self.url_redirect is None:
            return reverse_lazy('login')
        return self.url_redirect
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perms(self.get_perms()):
            return super().dispatch(request, *args, **kwargs)
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect(self.get_url_redirect())
    
    
    