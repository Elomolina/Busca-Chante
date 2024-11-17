from django.urls import path
from . import views
urlpatterns=[
    path('', views.Index.as_view(), name="index"),
    path('crearPost/', views.CrearPost.as_view(), name="create_post"),
    path('buscarEspacio/', views.buscarEspacio.as_view(), name="buscar_espacio"),
    path('espacioDetallado/<int:id>/', views.EspacioDetallado.as_view(), name = "espacio_detallado"),
    path('recomendarEspacio/<int:id>/', views.RecomendarEspacio.as_view(), name = "recomendar_espacio")
]