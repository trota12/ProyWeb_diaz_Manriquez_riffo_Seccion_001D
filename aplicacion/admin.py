from django.contrib import admin
from .models import Categoria, Producto, PerfilUsuario, Pedido, DetallePedido, Pago



# Register your models here.


admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(PerfilUsuario)
admin.site.register(Pedido)
admin.site.register(DetallePedido)
admin.site.register(Pago)

class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'direccion', 'telefono')  # Campos visibles en el admin
    search_fields = ('usuario__username', 'direccion', 'telefono')  # Búsqueda rápida
    fields = ('usuario', 'direccion', 'telefono')  # Campos en el formulario de edición