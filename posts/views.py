from django.http import HttpResponse, JsonResponse
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
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        posts = []
        casas_renta = RentarCasa.objects.all().order_by("-fecha")
        for i in casas_renta:
            informacion = {}
            imagenes = []
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
            "posts": posts
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
            "comentarios": comentarios
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
            "espacios_disponibles": informacion_espacios
        })
    def post(self, request, id):
        data = json.loads(request.body)
        post = BuscarCasa.objects.get(pk = id)
        autor = UserInfo.objects.get(user = request.user)
        for i in data:
            postOferta = RentarCasa.objects.get(pk = i)
            oferta = ofertasBusqueda(post = post,postOferta = postOferta ,autor = autor)
            oferta.save()
            print("oferta guardada")
        
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
            "buscar_espacio": busqueda
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
        return render(request, "post/create_post.html")
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
            print(key)
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