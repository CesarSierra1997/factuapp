from django.contrib import admin
from .models import *
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class UsuarioResource(resources.ModelResource):
    class Meta:
        model = Usuario

class UsuarioAdmin(admin.ModelAdmin):

    search_fields = ('nombres','apellidos')
    list_display = ('nombres','apellidos','is_active','is_staff')
    resource_class = UsuarioResource
    actions = ['eliminacion_logica','activacion_logica']

    def eliminacion_logica(self, request, queryset):
        for usuario in queryset:
            usuario.is_active = False
            usuario.save()

    def activacion_logica(self, request, queryset):
        for usuario in queryset:
            usuario.is_active = True
            usuario.save()

    def get_actions(self, request):
        actions = super().get_actions(request)
        # if 'delete_selected' in actions: # Elimina la acción de eliminación selección
        #     del actions['delete_selected']
        return actions
    
# Register your models here.
admin.site.register(Usuario, UsuarioAdmin),
admin.site.register(Permission),
# admin.site.register(ContentType),

