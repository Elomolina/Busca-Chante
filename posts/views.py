from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View


# Create your views here.
class Index(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        print(request.user)
        return render(request, "post/index.html")
    def post(self, request):
        pass

class CrearPost(View):
    def get(self, request):
        return render(request, "post/create_post.html")
    def post(self, request):
        pass