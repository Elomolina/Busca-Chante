from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
class Index(View):
    def get(self, request):
        print(request.user)
        return HttpResponse(f"holi {request.user}")
    def post(self, request):
        pass