from django.contrib import admin
from .models import Wartungsart, Wartungsvorgang, Wartungszuordnung

# Register your models here.
@admin.register(Wartungsart)
class WartungsartAdmin(admin.ModelAdmin):
    list_display = ("name", "kategorie")
    list_filter = ("kategorie", "aktiv")
    search_fields = ("name",)
    ordering = ("name",)

@admin.register(Wartungszuordnung)
class WartungszuordnungAdmin(admin.ModelAdmin):
    list_display = ("wartungsart", "fahrzeug", "geraet", "letzte_wartung", "naechste_wartung", "aktiv")
    list_filter = ("aktiv", "wartungsart__kategorie")
    search_fields = ("fahrzeug__bezeichnung", "geraet__identifikation", "wartungsart__name")
    readonly_fields = ("naechste_wartung",)  # Wird automatisch berechnet

@admin.register(Wartungsvorgang)
class WartungsvorgangAdmin(admin.ModelAdmin):
    list_display = ("zuordnung", "fahrzeug_name", "zuordnung__geraet", "wartungsart_name", "datum", "abschluss_datum", "status", "aktiv")
    list_filter = ("status", "aktiv", "datum")
    search_fields = ("fahrzeug_name", "geraet_name", "zuordnung__geraet", "durchgeführt_von")