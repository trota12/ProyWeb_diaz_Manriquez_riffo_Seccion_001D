from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from .views import iniciar_pago, respuesta, admin_login, vista_admin, agregar_producto, editar_producto, eliminar_producto, ProductoViewSet, CategoriaViewSet, PedidoViewSet

from rest_framework.routers import DefaultRouter
from .views import editar_perfil
from .views import PedidoSerializer
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'categorias', CategoriaViewSet)

router.register(r'pedidos', PedidoViewSet, basename='pedidos')




urlpatterns = [
    path('', views.index, name='index'),
    path('quienes-somos/', views.quienes_somos, name='quienes_somos'),
    path('vision/', views.vision, name='vision'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('producto_detalle/<int:producto_id>/', views.producto_detalle, name='producto_detalle'),  
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar-del-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('buscar/', views.buscar_producto, name='buscar_producto'),
    path('webpay/iniciar_pago/', iniciar_pago, name='iniciar_pago'),
    path('webpay/respuesta/', respuesta, name='respuesta'),
    path('admin_login/', admin_login, name='admin_login'),
    path('vista_admin/', vista_admin, name='vista_admin'),
    path('vista_admin/agregar/', agregar_producto, name='agregar_producto'),
    path('vista_admin/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('vista_admin/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('api/', include(router.urls)),
    path('editar-perfil/', editar_perfil, name='editar_perfil'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)