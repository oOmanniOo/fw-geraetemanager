from django.contrib import admin
from .models import Fahrzeug, Geraeteraum

@admin.register(Fahrzeug)
class FahrzeugAdmin(admin.ModelAdmin):
    list_display = ('bezeichnung', 'kennzeichen', 'funkrufname', 'standort', 'aktiv')
    list_filter = ('aktiv',)

    @admin.register(Geraeteraum)
    class GeraeteraumAdmin(admin.ModelAdmin):
        list_display = ('bezeichnung', 'fahrzeug')
        list_filter = ('fahrzeug',)
        search_fields = ('bezeichnung', 'fahrzeug__bezeichnung')
        list_per_page = 25
        ordering = ('bezeichnung',)
