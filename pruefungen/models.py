from django.db import models
from geraete.models import Geraetekategorie, Geraet

from dateutil.relativedelta import relativedelta

# Create your models here.
class Pruefungsart(models.Model):
    name = models.CharField(max_length=255)
    beschreibung = models.TextField(blank=True, null=True)
    intervall_monate = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Anzahl Monate bis zur nächsten Prüfung (leer lassen, wenn kein Intervall)"
    )
    
    def __str__(self):
        return self.name

class Checkliste(models.Model):
    name = models.CharField(max_length=255)
    art = models.ForeignKey(Pruefungsart, on_delete=models.CASCADE)
    kategorie = models.ForeignKey(Geraetekategorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Checklistenpunkt(models.Model):
    checkliste = models.ForeignKey(Checkliste, on_delete=models.CASCADE, related_name='punkte')
    name = models.CharField(max_length=255)
    ist_pflicht = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Pruefung(models.Model):
    geraet = models.ForeignKey(Geraet, on_delete=models.CASCADE)
    art = models.ForeignKey(Pruefungsart, on_delete=models.CASCADE)
    datum = models.DateField()
    pruefer = models.CharField(max_length=255)
    bestanden = models.BooleanField(null=True, blank=True)
    bemerkung = models.TextField(blank=True)

    def __str__(self):
        return f"{self.geraet.bezeichnung} - {self.art.name} durchgeführt am {self.datum}"
    
    @property
    def naechste_pruefung(self):
        """Berechnet das nächste Prüfungsdatum auf Basis des Monatsintervalls."""
        if self.art.intervall_monate:
            return self.datum + relativedelta(months=self.art.intervall_monate)
        return None

class Antwort(models.Model):
    pruefung = models.ForeignKey(Pruefung, on_delete=models.CASCADE, related_name='antworten')
    punkt = models.ForeignKey(Checklistenpunkt, on_delete=models.CASCADE)
    ok = models.BooleanField(default=False)
    bemerkung = models.TextField(blank=True)
    class Meta:
        unique_together = ('pruefung', 'punkt')