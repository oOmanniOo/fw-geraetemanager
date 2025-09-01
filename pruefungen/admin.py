from django.contrib import admin
from .models import Pruefungsart, Checkliste, Checklistenpunkt, Pruefung, Antwort

# Register your models here.

admin.site.register(Pruefungsart)
admin.site.register(Checklistenpunkt)
admin.site.register(Pruefung)
admin.site.register(Antwort)

class ChecklistenpunktInline(admin.TabularInline):
    model = Checklistenpunkt
    extra = 1

@admin.register(Checkliste)
class ChecklisteAdmin(admin.ModelAdmin):
    inlines = [ChecklistenpunktInline]