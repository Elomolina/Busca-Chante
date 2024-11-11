from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
import json
from .models import *
from django.shortcuts import render
from django.views import View

@method_decorator(csrf_exempt, name = 'dispatch')
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("index"))
        return render(request, "authentication/login.html")
    def post(self, request):
        data = json.loads(request.body)
        #check mail or user
        try:
            user = User.objects.get(Q(email = data['user_mail']) | Q(username = data['user_mail']))
            username = user.username
            #authentication to check pass
            u = authenticate(request, username = username, password = data['password'])
            if u is None:
                return JsonResponse({"error": "La contraseña no es correcta"})
            login(request, u)
            return JsonResponse({"success": "Bienvenido al Busca Chante 🤠", "path": "/"})      
        except User.DoesNotExist:
            return JsonResponse({"error": "El usuario no existe 😯"})
        

@method_decorator(csrf_exempt, name = 'dispatch')
class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse("index"))
        return render(request, "authentication/register.html")
    def post(self, request):
        data = json.loads(request.body)
        #chequear si correo ta ahi 
        correo = User.objects.filter(email = data['correo'])
        if len(correo) > 0:
            return JsonResponse({"error": "Este correo ya fue registrado 🦔"})
        #chequear num telefono
        try:
            user_phone = UserInfo.objects.get(phone_number = data['telefono'])
            return JsonResponse({"error": "Este número de teléfono ya fue registrado 🦔"})
        except UserInfo.DoesNotExist:
            try:
                #registramos user y guardamos telefono
                user = User.objects.create_user(email = data['correo'], password = data['password'], username=data['username'], last_name = data['apellido'], first_name = data['nombre'])
                user_info = UserInfo(user = user, phone_number = data['telefono'])
                user_info.save()
                #guardamos user en la session
                login(request, user)
            except IntegrityError:
                return JsonResponse({"error": "Este usuario ya existe 🦔"})
        return JsonResponse({"success": "Bienvenido al Busca Chante 🤠", "path": "/"})