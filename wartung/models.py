from django.db import models
from django.core.exceptions import ValidationError

from fahrzeuge.models import Fahrzeug
from geraete.models import Geraet

from dateutil.relativedelta import relativedelta
from datetime import date

class  Wartungsart(models.Model):
    KATEGORIE_AUSWAHL = [
        ("FAHRZEUG", "Fahrzeug"),
        ("GERAET", "Gerät"),
        ("BEIDES", "Gerät und Fahrzeug"),
    ]

    name = models.CharField(max_length=150, blank=False, null=False)
    beschreibung = models.TextField(blank=True, null=True)
    intervall_monate =  models.PositiveSmallIntegerField()
    kategorie = models.CharField(
        max_length=30,
        choices=KATEGORIE_AUSWAHL
    )
    aktiv = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} für {self.kategorie}"
    
    class Meta:
        verbose_name = "Wartungsart"
        verbose_name_plural = "Wartungsarten"

class Wartungszuordnung(models.Model):
    wartungsart = models.ForeignKey(Wartungsart, on_delete=models.CASCADE)
    fahrzeug = models.ForeignKey(Fahrzeug, on_delete=models.CASCADE, null=True, blank=True)
    geraet = models.ForeignKey(Geraet, on_delete=models.CASCADE, null=True, blank=True)

    letzte_wartung = models.DateField(null=True, blank=True)
    naechste_wartung = models.DateField(null=True, blank=True)
    bemerkung = models.TextField(null=True, blank=True)
    aktiv = models.BooleanField(default=True)

    def clean(self):
        if not self.fahrzeug and not self.geraet:
            raise ValidationError("Es muss ein Fahrzeug oder ein Gerät angegeben werden.")
        if self.fahrzeug and self.geraet:
            raise ValidationError("Eine Zuordnung darf nicht gleichzeitig ein Fahrzeug und ein Gerät enthalten.")

    def __str__(self) -> str:
        ziel = self.fahrzeug or self.geraet
        return f"{self.wartungsart} für {ziel}"
    
    def berechnung_naechste_wartung(self):
        if not self.letzte_wartung:
            return None        
        return self.letzte_wartung + relativedelta(months=self.wartungsart.intervall_monate)
    
    def save(self, *args, **kwargs):
        #Beim Speichern das nächste Waruntungsdatum aktualisieren
        if self.letzte_wartung:
            self.naechste_wartung = self.berechnung_naechste_wartung()

        super().save(*args, **kwargs)  

class Wartungsvorgang(models.Model):
    STATUS_AUSWAHL = [
        ("offen", "Offen"),
        ("in_arbeit", "In Arbeit"),
        ("abgeschlossen", "Abgeschlossen"),
    ]

    zuordnung = models.ForeignKey(
        Wartungszuordnung,
        on_delete=models.SET_NULL,
        related_name= "vorgaenge",
        help_text="Bezieht sich auf eine bestimmte Wartungszuordnung (Fahrzeug/Gerät + Wartungsart).",
        null=True,
        blank=True,
    )

    datum = models.DateField(
        auto_now_add=True,
        help_text="Datum, an dem die Wartung angelegt oder durchgeführt wurde."
    )

    abschluss_datum = models.DateField(null=True, blank=True, help_text="Datum an dem die Wartung abgeschlossen worden ist.")

    status = models.CharField(
        max_length=20,
        choices=STATUS_AUSWAHL,
        default="offen",
        help_text="Status des Wartungsvorgangs",
    )

    durchgefuehrt_von = models.CharField(
        max_length=100,
        blank = True, 
        null= True,
        help_text="Person die die Wartung durchgeführt hat"
    )

    bemerkung = models.TextField(blank=True, null=True, help_text="Freitextfeld für zusätzliche Hinweise oder Beobachtungen.")

    aktiv = models.BooleanField(default=True)

    fahrzeug_name = models.CharField(max_length=150, blank=True, null=True)
    geraet_name = models.CharField(max_length=150, blank=True, null=True)
    wartungsart_name = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self) -> str:
        return f"Wartung {self.zuordnung} am {self.datum}"
    
    def save(self, *args, **kwargs):
        if self.zuordnung:
            self.fahrzeug_name = str(self.zuordnung.fahrzeug) if self.zuordnung.fahrzeug else None
            self.geraet_name = str(self.zuordnung.geraet) if self.zuordnung.geraet else None
            self.wartungsart_name = str(self.zuordnung.wartungsart)
        # Wenn die Wartung abgeschlossen wird, setze das Datum der letzten Wartung in der Zuordnung
        if self.status == "abgeschlossen" and self.zuordnung:
            self.abschluss_datum = date.today()
            self.zuordnung.letzte_wartung = self.abschluss_datum
            self.zuordnung.naechste_wartung = self.zuordnung.berechnung_naechste_wartung()
            self.zuordnung.save()
        super().save(*args, **kwargs)
