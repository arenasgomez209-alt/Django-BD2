from django.contrib import admin
from django.urls import path
from proveedores.views import home, log, Registeruser, logoutuser, Proinsertar, Promostrar, Proeditar, Proeliminarss, Proeliminar, inicio

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('inicio', inicio),
    path('User/login', log),
    path('User/registro', Registeruser),
    path('User/salir', logoutuser),
    path('Proveedor/insertar', Proinsertar),
    path('Proveedor/mostrar', Promostrar),
    path('Proveedor/editar/<str:idpro>', Proeditar),
    path('Proveedor/eliminars/<str:idpro>', Proeliminarss),
    path('Proveedor/eliminar', Proeliminar),
]
