from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from aplicacion.models import PerfilUsuario
from .forms import CustomAuthenticationForm, ProductoForm
from .models import Producto, ItemCarrito, Pedido
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import JsonResponse
from transbank.webpay.webpay_plus.transaction import Transaction
from django.contrib import messages
from rest_framework import viewsets, filters
from .models import Producto, Categoria, Pedido
from .serializers import ProductoSerializer, CategoriaSerializer, PedidoSerializer

# Vistas normales
def index(request):
    return render(request, 'index.html')

def quienes_somos(request):
    return render(request, 'quienes_somos.html')

def catalogo(request):
    productos = Producto.objects.all()  # Obtiene todos los productos disponibles
    return render(request, 'catalogo.html', {'productos': productos})

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'producto_detalle.html', {'producto': producto})

def agregar_al_carrito(request):
    return render(request, 'agregar_al_carrito.html')

def buscar_producto(request):
    query = request.GET.get('q', '')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.none()

    return render(request, 'catalogo.html', {'productos': productos})


def vision(request):
    return render(request, 'vision.html')

# Vista de registro
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name', '')  #  get para evitar KeyError
            user.last_name = form.cleaned_data.get('last_name', '')  
            user.save()

            login(request, user)
            return redirect('index') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# LOGIN
def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# CIERRE SESIÓN
def custom_logout(request):
    logout(request)
    return redirect('login')  # Redirige al login después de cerrar sesión


#CARRITO
@login_required
def ver_carrito(request):
    items = ItemCarrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in items)
    
    cart_count = sum(item.cantidad for item in items)  

    if request.method == 'POST':
        if 'eliminar' in request.POST:
            item_id = request.POST.get('eliminar')
            item = ItemCarrito.objects.get(id=item_id, usuario=request.user)
            item.delete()
            return redirect('ver_carrito')
    
    if not items:
        return render(request, 'carrito_vacio.html', {"cart_count": cart_count})

    return render(request, 'carrito.html', {'items': items, 'total': total, 'cart_count': cart_count})

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    item, created = ItemCarrito.objects.get_or_create(usuario=request.user, producto=producto)
    if not created:
        if item.cantidad < item.producto.stock:
            item.cantidad += 1
            item.save()

    request.session.modified = True
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = ItemCarrito.objects.filter(usuario=request.user).count()
        return JsonResponse({'cart_count': cart_count})
    else:
        return redirect('ver_carrito')



@login_required
def eliminar_del_carrito(request, item_id):
    item = ItemCarrito.objects.get(id=item_id, usuario=request.user)
    item.delete()
    return redirect('ver_carrito')


#WEBPAY

def iniciar_pago(request):
    if not request.user.is_authenticated:
        return redirect("login")

    items = ItemCarrito.objects.filter(usuario=request.user)
    if not items:
        return redirect("ver_carrito")  # Si el carrito está vacío, redirige

    total = sum(item.producto.precio * item.cantidad for item in items)

    tx = Transaction()
    buy_order = f"Orden-{request.user.id}-01-{Pedido.objects.filter(usuario=request.user).count() + 1}2025"
    session_id = str(request.user.id)
    return_url = request.build_absolute_uri("/webpay/respuesta/")


    response = tx.create(buy_order, session_id, total, return_url)

    #Guardar transacción en la BD
    pedido = Pedido.objects.create(usuario=request.user, total=total, estado="pendiente")
    
    return redirect(response["url"] + "?token_ws=" + response["token"])

def respuesta(request):
    token = request.GET.get("token_ws", None)
    if not token:
        return redirect("ver_carrito")  # Si no hay token, redirigir al carrito

    tx = Transaction()
    response = tx.commit(token)

    if response["status"] == "AUTHORIZED":
        pedido = Pedido.objects.filter(usuario=request.user, estado="pendiente").first()

        if pedido:
            items = ItemCarrito.objects.filter(usuario=request.user)

            for item in items:
                producto = item.producto
                if producto.stock >= item.cantidad:  # Verificar que hay suficiente stock
                    producto.stock -= item.cantidad  # Restar el articulo comprado
                    producto.save()
                else:
                    messages.error(request, f"No hay suficiente stock de {producto.nombre}.")
                    return redirect("ver_carrito")

            pedido.estado = "pagado"
            pedido.transaction_id = token
            pedido.save()

            # Vaciar el carrito despúes de la compra
            items.delete()
            request.session["cart_count"] = 0  # Reiniciar contador del carrito

            return render(request, "webpay/exito.html", {"response": response})

    return render(request, "webpay/error.html", {"response": response})
    
#ADMIN

def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('vista_admin')  # Si esta autenticado, redirigir al panel de administracion

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_superuser:
                login(request, user)
                return redirect('vista_admin')  # Redirigir al panel de administración
            else:
                messages.error(request, "No tienes permisos de administrador.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    
    return render(request, "registration/admin_login.html", {"form": form})

def solo_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(solo_admin)
def vista_admin(request):
    productos = Producto.objects.all()
    return render(request, 'vista_admin.html', {'productos': productos})

@login_required
@user_passes_test(solo_admin)
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vista_admin')
    else:
        form = ProductoForm()
    return render(request, "administracion.html", {"form": form})

@login_required
@user_passes_test(solo_admin)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('vista_admin')
    else:
        form = ProductoForm(instance=producto)
    return render(request, "administracion.html", {"form": form, "producto": producto})

@login_required
@user_passes_test(solo_admin)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('vista_admin')




#CREACION DE API


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['precio', 'nombre']

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer