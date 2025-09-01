from django.db import models

# Create your models here.
class Fahrzeug(models.Model):
    bezeichnung = models.CharField(max_length=255)
    kennzeichen = models.CharField(max_length=20)
    funkrufname = models.CharField(max_length=20)
    standort = models.CharField(max_length=100)
    aktiv = models.BooleanField(default=True)
    bemerkung = models.TextField(blank=True)

    def __str__(self):
        return self.bezeichnung
    

class Geraeteraum(models.Model):
    bezeichnung = models.CharField(max_length=255)

    def __str__(self):
        return self.bezeichnung

