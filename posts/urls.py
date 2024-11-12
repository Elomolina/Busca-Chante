from django.urls import path
from . import views
urlpatterns=[
    path('', views.Index.as_view(), name="index"),
    path('crearPost/', views.CrearPost.as_view(), name="create_post")
]