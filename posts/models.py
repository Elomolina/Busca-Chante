from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from authentication.models import * 
from django.utils.timezone import now

tipos_casa = {
    "CCA": "Casa Completa", 
    "ACA": "Apartamento Completo", 
    "HP": "Habitación Privado", 
    "HC": "Habitación Compartida",
    "CCO": "Casa Compartida",
    "ACO": "Apartamento Compartido"
}
# Create your models here.
class TiposCasa(models.Model):
    tipo = models.CharField(choices=tipos_casa, max_length=20)
    def __str__(self):
        return f"{self.tipo}"

class BuscarCasa(models.Model):
    tipoCasa = models.ForeignKey(TiposCasa, on_delete=models.CASCADE, related_name="tipo_casaBusqueda")
    rangoPrecio = models.IntegerField(validators=[MaxValueValidator(50000), MinValueValidator(0)])
    ubicacion = models.TextField()
    descripcion = models.TextField()
    #revisar todas las casas que busque
    fecha = models.DateTimeField(default=now)
    autor = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="autorBusqueda")

class RentarCasa(models.Model):
    tipoCasa = models.ForeignKey(TiposCasa, on_delete=models.CASCADE, related_name="tipo_casaRenta")
    precio = models.IntegerField()
    cantidad_personas = models.IntegerField()
    ubicacion = models.TextField()
    descripcion = models.TextField()
    owner = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name="ownerCasa")
    fecha = models.DateTimeField(default=now)
    lugares_importantes = models.TextField()
    reglas_casa = models.TextField()
    def __str__(self):
        return f"{self.tipoCasa}, {self.precio}, {self.cantidad_personas}, {self.ubicacion}, {self.descripcion}, {self.owner}, {self.fecha}, {self.lugares_importantes}, {self.reglas_casa}"

class ImagenesRenta(models.Model):
    casa = models.ForeignKey(RentarCasa, on_delete=models.CASCADE, related_name="imagenesCasa")
    imagen = models.ImageField(upload_to="imagenes_renta")