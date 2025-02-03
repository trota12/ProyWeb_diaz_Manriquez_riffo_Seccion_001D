from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Categoria productos
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre 

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
    precio = models.IntegerField(default=0)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class ItemCarrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.cantidad > self.producto.stock:
            raise ValueError("No hay suficiente stock disponible.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} de {self.producto.nombre}"

# USUARIO
class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.usuario.username

# PEDIDO
class Pedido(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("pagado", "Pagado"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)  # Para Webpay

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario.username}"

# DETALLE PEDIDO
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="detalles")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} - Pedido {self.pedido.id}"

# PAGO
class Pago(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, unique=True)  # ID de la transacción Webpay
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[("exitoso", "Exitoso"), ("fallido", "Fallido")], default="exitoso")

    def __str__(self):
        return f"Pago {self.transaction_id} - Pedido {self.pedido.id}"
