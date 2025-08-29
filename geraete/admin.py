from django.contrib import admin
from .models import Geraet, Geraetekategorie, Status

@admin.register(Geraet)
class GeraetAdmin(admin.ModelAdmin):
    list_display = ('bezeichnung', 'identifikation', 'seriennummer', 'barcode', 'kategorie', 'status', 'geraeteraum', 'bemerkung')
    list_filter = ('kategorie', 'status', 'geraeteraum')
    search_fields = ('bezeichnung', 'identifikation', 'seriennummer', 'barcode')
    list_editable = ('status',)
    list_per_page = 25
    ordering = ('bezeichnung',)

@admin.register(Geraetekategorie)
class GeraetekategorieAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)