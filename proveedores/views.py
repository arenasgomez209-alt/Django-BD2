from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import connection

def home(request):
    return redirect('/User/login')

def inicio(request):
    if not request.user.is_authenticated:
        return redirect('/User/login')
    return render(request, 'Proveedor/home.html')

def log(request):
    if request.method == "POST":
        user = authenticate(username=request.POST.get('usu'), password=request.POST.get('pass'))
        if user is not None:
            login(request, user)
            return redirect('/inicio')
            #print("correcto")
        else:
            mensajeerror="Usuario o contraseña incorrecta, intente de nuevo"
            return render(request, 'Usuarios/login.html', {'mensajeerror': mensajeerror})
            #print ("Incorrecto...")
    return render(request, 'Usuarios/login.html')

def Registeruser(request):
    if request.method == "POST":
        # validar que viene por post y que todos los campos esten llenos
        if request.POST.get('usu') and request.POST.get('email') and request.POST.get('pass'):
            Usuario = User.objects.create_user(
                request.POST.get('usu'),
                request.POST.get('email'),
                request.POST.get('pass')
            )
            # En la vista de login solo pedimos Nombre (usu), Email y Contraseña. 
            # Si tuvieras 'nombre' y 'apellido' en el HTML, podrías guardarlos así:
            # Usuario.first_name = request.POST.get('nombre')
            # Usuario.last_name = request.POST.get('apellido')
            Usuario.save()
            return redirect('/User/login')
    return redirect('/User/login')

def logoutuser(request):
    logout(request)
    return redirect('/User/login')

def Proinsertar(request):
    if not request.user.is_authenticated:
        return redirect('/User/login')
    if request.method=="POST": #validar que viene por post
        if request.POST.get('nombre') and request.POST.get('direccion') and request.POST.get('nit') and request.POST.get('email') and request.POST.get('observaciones'): #validar que todos los campos viene llenos
            nombre=request.POST.get('nombre')
            direccion=request.POST.get('direccion')
            nit=request.POST.get('nit')
            email=request.POST.get('email')
            observaciones=request.POST.get('observaciones')
            insertar=connection.cursor()
            insertar.execute("call p_insertarproveedor(%s,%s,%s,%s,%s)", [nombre, direccion,nit,email,observaciones])
            #nombre del procedimiento almacenado
            return redirect('/Proveedor/mostrar')
        else:
            nombre=request.POST.get('nombre')
            direccion=request.POST.get('direccion')
            nit=request.POST.get('nit')
            email=request.POST.get('email')
            observaciones=request.POST.get('observaciones')
            mensa='Señor usuario falta datos'
            return render(request,'Proveedor/insertar.html',{'nombre':nombre,'direccion':direccion,
            'nit':nit,'email':email,'observaciones':observaciones,'mensa':mensa})
    else:
        return render(request,'Proveedor/insertar.html')

def Promostrar(request):
    if not request.user.is_authenticated:
        return redirect('/User/login')
    mostrar=connection.cursor()
    mostrar.execute("call p_mostrarproveedores()")
    #nombre del procedimiento almacenado
    return render(request,'Proveedor/mostrar.html',{'mostrar': mostrar})

def Proeditar(request, idpro):
    if not request.user.is_authenticated:
        return redirect('/User/login')
    if request.method=="POST": #validar que viene por post
        if request.POST.get('nombre') and request.POST.get('direccion') and request.POST.get('nit') and request.POST.get('email') and request.POST.get('observaciones'): #validar que todos los campos viene llenos
            nombre=request.POST.get('nombre')
            direccion=request.POST.get('direccion')
            nit=request.POST.get('nit')
            email=request.POST.get('email')
            observaciones=request.POST.get('observaciones')
            insertar=connection.cursor()
            insertar.execute("call p_editarproveedor(%s,%s,%s,%s,%s,%s)", [nombre, direccion,nit,email,observaciones,idpro])
            #nombre del procedimiento almacenado
            return redirect('/Proveedor/mostrar')
    else:
        proveedor=connection.cursor()
        proveedor.execute("call p_consuproveedor('"+idpro+"')")
        proveedor=proveedor.fetchone()
        # return render(request,'Proveedor/editar.html',{'prover':proveedor})
        return render(request,'Proveedor/editars.html',{'prover':proveedor})

def Proeliminarss(request, idpro):
    if not request.user.is_authenticated:
        return redirect('/User/login')
    eliminar=connection.cursor()
    eliminar.execute("call p_eliminarproveedor(%s)", [idpro])
    #nombre del procedimiento almacenado
    return redirect('/Proveedor/mostrar')

def Proeliminar(request):
    if not request.user.is_authenticated:
        return redirect('/User/login')
    idpro=request.POST.get('idprover')
    eliminar=connection.cursor()
    eliminar.execute("call p_eliminarproveedor(%s)", [idpro])
    #nombre del procedimiento almacenado
    return redirect('/Proveedor/mostrar')
