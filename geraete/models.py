from django.db import models
from fahrzeuge.models import Fahrzeug

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=255)
    beschreibung = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Geraetekategorie(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Geraet(models.Model):
    bezeichnung = models.CharField(max_length=100)
    identifikation = models.CharField(max_length=100, unique=True)
    seriennummer = models.CharField(max_length=100, blank=True, null=True)
    barcode = models.CharField(max_length=100, unique=True, blank=True, null=True)
    kategorie = models.ForeignKey(Geraetekategorie, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    fahrzeug = models.ForeignKey(Fahrzeug, on_delete=models.CASCADE)
    bemerkung = models.TextField(blank=True)
    erstellt_am = models.DateTimeField(auto_now_add=True)
    geaendert_am = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['kategorie', 'bezeichnung']

    def __str__(self):
        return f"{self.bezeichnung} ({self.identifikation})"
        