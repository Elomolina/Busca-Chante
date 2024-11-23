from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
import json
from .models import *
from authentication.models import *


class Index(View):
    def get(self, request):
        #crear sesion
        if 'guardados' not in request.session:
            request.session['guardados'] = []
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        posts = []
        casas_renta = RentarCasa.objects.all().order_by("-fecha")
        for i in casas_renta:
            informacion = {}
            imagenes = []
            for guardado in request.session.get('guardados'):
                if guardado['postID'] == i.id:
                    informacion['guardado'] = guardado['guardado']
            informacion['tipoCasa'] = tipos_casa[i.tipoCasa.tipo]
            informacion['ubicacion'] = i.ubicacion
            informacion['precio'] = i.precio 
            informacion['fecha'] = i.fecha
            informacion['owner'] = i.owner
            informacion['id'] = int(i.id)
            for image in i.imagenesCasa.all():
                imagenes.append(image)
            informacion['imagenes'] = imagenes
            posts.append(informacion)
        return render(request, "post/index.html", {
            "posts": posts, 
            "profile_pic": UserInfo.objects.get(user = request.user).profile_pic
        })

@method_decorator(csrf_exempt, name = 'dispatch')
class EspacioDetallado(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        espacio_detallado = RentarCasa.objects.get(pk = id)
        tipo_casa = tipos_casa[espacio_detallado.tipoCasa.tipo]
        imagenes = espacio_detallado.imagenesCasa.all()
        comentarios = ComentariosRenta.objects.filter(post = espacio_detallado)
        return render(request, "post/detailPost.html", {
            "id":id, 
            "tipo_casa": tipo_casa,
            "imagenes": imagenes,
            "espacio_detallado": espacio_detallado,
            "comentarios": comentarios,
            "profile_pic": UserInfo.objects.get(user = request.user).profile_pic
        })
    def post(self, request, id):
        data = json.loads(request.body)
        casa = RentarCasa.objects.get(pk = data['postID'])
        usuario = UserInfo.objects.get(user_id = data['userID'])
        comentario = ComentariosRenta(post = casa, comentario = data['message'], autor = usuario)
        comentario.save()
        return JsonResponse({'sucess': 'Comentario agregado'})
    
@method_decorator(csrf_exempt, name = 'dispatch')
class RecomendarEspacio(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        busqueda = BuscarCasa.objects.get(pk = id)
        tipo_casa = tipos_casa[busqueda.tipoCasa.tipo]
        #casas que tengo yo en renta
        user = UserInfo.objects.get(user = request.user)
        espacios_disponibles = RentarCasa.objects.filter(owner = user)
        informacion_espacios = []
        for i  in espacios_disponibles:
            info = {}
            imagenes = []
            info['tipo'] = tipos_casa[i.tipoCasa.tipo]
            info['precio'] = i.precio
            info['id'] = i.id
            for img in i.imagenesCasa.all():
                imagenes.append(img)
            info['imagenes'] = imagenes
            informacion_espacios.append(info)
        #falta
        offer = ofertasBusqueda.objects.filter(post = busqueda).order_by("-fecha")
        ofertas = []
        for i in offer:
            info = {}
            info['post'] = i.post
            info['postOferta'] = i.postOferta
            info['autor'] = i.autor 
            info['fecha'] = i.fecha
            info['id'] = i.id
            #solo una imagen
            info['imagen'] = i.postOferta.imagenesCasa.all()[0]
            ofertas.append(info)
        return render(request, "post/recomendarEspacio.html", {
            "busqueda": busqueda, 
            "tipo_casa": tipo_casa, 
            "ofertas": ofertas,
            "espacios_disponibles": informacion_espacios,
            "profile_pic": UserInfo.objects.get(user = request.user).profile_pic
        })
    def post(self, request, id):
        data = json.loads(request.body)
        post = BuscarCasa.objects.get(pk = id)
        autor = UserInfo.objects.get(user = request.user)
        for i in data:
            postOferta = RentarCasa.objects.get(pk = i)
            oferta = ofertasBusqueda(post = post,postOferta = postOferta ,autor = autor)
            oferta.save()
        
        ofertas = ofertasBusqueda.objects.all()
        #ofertas = ofertasBusqueda()
        return JsonResponse({"success": "Oferta realizada 😎"})

@method_decorator(csrf_exempt, name = 'dispatch')
class borrarOferta(View):
    def post(self, request):
        data = json.loads(request.body)
        oferta = ofertasBusqueda.objects.get(pk = data)
        oferta.delete()
        return JsonResponse({'success': 'oferta borrada 🕵️'})
    
class buscarEspacio(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        buscar_espacio = BuscarCasa.objects.all().order_by("-fecha")
        busqueda = []
        for i in buscar_espacio:
            info = {}
            info['id'] = i.id
            info['tipoCasa'] = tipos_casa[i.tipoCasa.tipo]
            info['rangoPrecio'] = i.rangoPrecio
            info['ubicacion'] = i.ubicacion
            info['descripcion'] = i.descripcion
            info['fecha'] = i.fecha
            info['autor'] = i.autor
            busqueda.append(info)
        return render(request, "post/buscarRenta.html", {
            "buscar_espacio": busqueda,
            "profile_pic": UserInfo.objects.get(user = request.user).profile_pic
        })

@method_decorator(csrf_exempt, name = 'dispatch')
class borrarEspacio(View):
    def post(self, request):
        data = json.loads(request.body)
        espacio =  RentarCasa.objects.get(pk = data)
        espacio.delete()
        return JsonResponse({"sucess": "El espacio ha sido borrado exitosamente"})

@method_decorator(csrf_exempt, name = 'dispatch')
class borrarBusqueda(View):
    def post(self, request):
        data = json.loads(request.body)
        busqueda =  BuscarCasa.objects.get(pk = data)
        busqueda.delete()
        return JsonResponse({"sucess": "El espacio ha sido borrado exitosamente"})

@method_decorator(csrf_exempt, name = 'dispatch')
class CrearPost(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        return render(request, "post/create_post.html", {
            "profile_pic": UserInfo.objects.get(user = request.user).profile_pic
        })
    def post(self, request):
        try:
            data = json.loads(request.POST.get('information'))
        except TypeError:
            data = json.loads(request.body)
        #pedimos las imagenes
        imagenes = request.FILES.getlist('files[]')
        key = ''
        if data['tipoInfo'] == 'buscar':
            for clave, valor in tipos_casa.items():
                if valor == data['tipoCasa']:
                    key = clave
                    break
            data['rangoPrecio'] = int(data['rangoPrecio'])
            tipo_casa = TiposCasa.objects.get(tipo = key)
            user_info = UserInfo.objects.get(user = request.user)
            buscar_casa = BuscarCasa(tipoCasa = tipo_casa, rangoPrecio = data['rangoPrecio'], ubicacion = data['ubicacion'], descripcion = data['descripcion'], autor = user_info)
            buscar_casa.save()
            return JsonResponse({"success": "Búsqueda subida 🥳", "path": "/"})
        elif data['tipoInfo'] == 'rentar':
            key = ''
            for clave, valor in tipos_casa.items():
                if valor == data['tipoCasa']:
                    key = clave
                    break
            #guardamos datos de renta
            tipo_casa = TiposCasa.objects.get(tipo = key)
            user_info = UserInfo.objects.get(user = request.user)
            rentar_casa = RentarCasa(tipoCasa = tipo_casa, precio = int(data['precio']), cantidad_personas = int(data['cantidad_personas']), ubicacion = data['ubicacion'], descripcion = data['descripcion'], owner = user_info, lugares_importantes = data['lugares_importantes'], reglas_casa = data['reglas_casa'])
            rentar_casa.save()
            #guardamos las imagenes
            for i in imagenes:
                imagenes_renta = ImagenesRenta(casa = rentar_casa, imagen = i)
                imagenes_renta.save()
            return JsonResponse({"success": "Espacio en renta subido 🥳", "path": "/"})

@method_decorator(csrf_exempt, name = 'dispatch')
class actualizarRenta(View):
    def post(self, request):
        data = json.loads(request.body)
        tipoCasa = data['tipoCasa']
        key = ''
        for clave, valor in tipos_casa.items():
            if valor == tipoCasa:
                key = clave
        tipo = TiposCasa.objects.get(tipo = key)
        actualizacion = RentarCasa.objects.filter(pk = data['postID']).update(tipoCasa = tipo.id,precio = int(data['precio']), cantidad_personas = int(data['cantidad']), ubicacion = data['ubicacion'], descripcion = data['descripcion'], lugares_importantes = data['rentarLugaresImportantes'] ,reglas_casa = data['reglasCasa'])
        return JsonResponse({"success": "Los datos han sido actualizados"})
    
@method_decorator(csrf_exempt, name = 'dispatch')
class actualizarBusqueda(View):
    def post(self, request):
        data = json.loads(request.body)
        tipoCasa = data['tipoCasa']
        key = ''
        for clave, valor in tipos_casa.items():
            if valor == tipoCasa:
                key = clave
        tipo = TiposCasa.objects.get(tipo = key)
        actualizacion = BuscarCasa.objects.filter(pk = data['buscarID']).update(tipoCasa = tipo.id, rangoPrecio = int(data['precio']), ubicacion = data['ubicacion'], descripcion = data['descripcion'])
        return JsonResponse({"success": "Los datos han sido actualizados"})

class misGuardados(View):
    def get(self, request):
        guardados = request.session.get('guardados')
        posts_guardados = []
        for i in guardados:
            info = {}
            imagenes = []
            renta = RentarCasa.objects.get(pk = i['postID'])
            info['tipoCasa'] = tipos_casa[renta.tipoCasa.tipo]
            info['ubicacion'] = renta.ubicacion
            info['precio'] = renta.precio
            info['fecha'] = renta.fecha
            info['owner'] = renta.owner 
            info['id'] = int(renta.id)
            for image in renta.imagenesCasa.all():
                imagenes.append(image)
            info['imagenes'] = imagenes
            posts_guardados.append(info)
        return render(request, "post/misGuardados.html", {
            "posts": posts_guardados,
            "profile_pic": UserInfo.objects.get(user = request.user).profile_pic
        })

@method_decorator(csrf_exempt, name = 'dispatch')   
class guardarPost(View):
    def post(self, request):
        data = json.loads(request.body)
        post = int(data['post'])
        info = {
            'guardado': data['saved'], 
            'postID': post
        }
        #desguardar
        if not data['saved']:
            guardados = request.session.get('guardados')
            for i in guardados:
                if i['postID'] == post:
                    guardados.remove(i)
                    break
            request.session['guardados'] = guardados
        else:
            request.session['guardados'] += [info]
        if data['path'] == '/misGuardados/':
            return JsonResponse({'recargar': 'True'})
        return JsonResponse({"recargar": "false"})
    
@method_decorator(csrf_exempt, name = 'dispatch')
class userProfile(View):
    def get(self, request):
        user_info = UserInfo.objects.get(user_id = request.user)
        return render(request, "post/userProfile.html", {
            "nombre": request.user.first_name, 
            "apellido": request.user.last_name,
            "telefono": user_info.phone_number,
            "profile_pic": user_info.profile_pic,
            "username": request.user.username
        })
    def post(self, request):
        data = json.loads(request.POST.get('informacion'))
        #actualizamos datos
        user = User.objects.filter(username = data['username']).update(username = data['username'], first_name = data['nombre'], last_name = data['apellido'])
        user_info = UserInfo.objects.filter(user = request.user).update(phone_number = int(data['telefono']))
        return JsonResponse({"success": "Datos actualizados"})

@method_decorator(csrf_exempt, name = 'dispatch')
class actualizarProfilePic(View):
    def post(self, request):
        data = request.FILES.getlist('file')
        for i in data:
            user = UserInfo.objects.get(user = request.user)
            user.profile_pic = i 
            user.save()
        return JsonResponse({"success": "Foto de perfil actualizada"})