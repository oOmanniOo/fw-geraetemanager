from django.contrib import admin
from .models import Fahrzeug

@admin.register(Fahrzeug)
class FahrzeugAdmin(admin.ModelAdmin):
    list_display = ('bezeichnung', 'kennzeichen', 'funkrufname', 'standort', 'aktiv')
    list_filter = ('aktiv',)
    search_fields = ('bezeichnung', 'kennzeichen', 'funkrufname', 'standort')
    list_editable = ('aktiv',)
    list_per_page = 25
    ordering = ('bezeichnung',)
    
