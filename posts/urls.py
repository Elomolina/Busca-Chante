from django.urls import path
from . import views
urlpatterns=[
    path('', views.Index.as_view(), name="index"),
    path('crearPost/', views.CrearPost.as_view(), name="create_post"),
    path('buscarEspacio/', views.buscarEspacio.as_view(), name="buscar_espacio"),
    path('espacioDetallado/<int:id>/', views.EspacioDetallado.as_view(), name = "espacio_detallado"),
    path('recomendarEspacio/<int:id>/', views.RecomendarEspacio.as_view(), name = "recomendar_espacio"),
    path('borrarOferta/', views.borrarOferta.as_view(), name = "borrarOferta"),
    path('borrarEspacio/', views.borrarEspacio.as_view(), name = "borrarEspacio"),
    path('borrarBusqueda/', views.borrarBusqueda.as_view(), name = "borrarBusqueda"),
    path('actualizarRenta/', views.actualizarRenta.as_view(), name = "actualizarRenta"),
    path('actualizarBusqueda/', views.actualizarBusqueda.as_view(), name = "actualizarBusqueda"),
    path('guardarPost/', views.guardarPost.as_view(), name = "guardarPost"),
    path('misGuardados/', views.misGuardados.as_view(), name = "misGuardados"),
    path('userProfile/', views.userProfile.as_view(), name = "userProfile"),
    path('actualizarProfilePic/', views.actualizarProfilePic.as_view(), name = "actualizarProfilePic"),
]