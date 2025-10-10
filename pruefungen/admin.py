from django.contrib import admin
from .models import Pruefungsart, Checkliste, Checklistenpunkt, Pruefung, Antwort
from django.contrib import messages

# --- Inline für Checklistenpunkte ---
class ChecklistenpunktInline(admin.TabularInline):
    model = Checklistenpunkt
    extra = 1
    fields = ("name", "ist_pflicht")
    verbose_name = "Prüfpunkt"
    verbose_name_plural = "Prüfpunkte"


# --- Prüfungsart ---
@admin.register(Pruefungsart)
class PruefungsartAdmin(admin.ModelAdmin):
    list_display = ("name", "intervall_monate", "kategorien_anzeigen")
    list_filter = ("geraetekategorie",)
    search_fields = ("name", "beschreibung")
    filter_horizontal = ("geraetekategorie",)
    ordering = ("name",)

    def kategorien_anzeigen(self, obj):
        return ", ".join([k.name for k in obj.geraetekategorie.all()])
    kategorien_anzeigen.short_description = "Kategorien" #type: ignore

    def save_model(self, request, obj, form, change):
        # Wenn die Prüfungsart bereits existiert und Kategorien geändert wurden
        if change:
            alte_kategorien = set(obj.__class__.objects.get(pk=obj.pk).geraetekategorie.all())
            neue_kategorien = set(form.cleaned_data["geraetekategorie"])
            entfernte = alte_kategorien - neue_kategorien

            for kat in entfernte:
                # Gibt es noch Checklisten, die diese Kombination verwenden?
                if Checkliste.objects.filter(art=obj, kategorie=kat).exists():
                    messages.error(
                        request,
                        f"Die Kategorie '{kat}' konnte nicht entfernt werden, "
                        f"weil noch Checklisten existieren, die '{obj.name}' und '{kat.name}' verwenden."
                    )
                    # Kategorie wieder hinzufügen, um Konsistenz zu wahren
                    obj.geraetekategorie.add(kat)

        super().save_model(request, obj, form, change)    

# --- Checkliste ---
@admin.register(Checkliste)
class ChecklisteAdmin(admin.ModelAdmin):
    list_display = ("name", "art", "kategorie")
    list_filter = ("art", "kategorie")
    search_fields = ("name",)
    inlines = [ChecklistenpunktInline]
    ordering = ("name",)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.kategorie not in obj.art.geraetekategorie.all():
            obj.art.geraetekategorie.add(obj.kategorie)
            messages.info(
                request,
                f"Die Kategorie '{obj.kategorie}' wurde automatisch zur Prüfungsart '{obj.art}' hinzugefügt."
            )

# --- Antwort (Ergebnis einzelner Punkte) ---
class AntwortInline(admin.TabularInline):
    model = Antwort
    extra = 0
    fields = ("punkt_name", "ok", "bemerkung")
    readonly_fields = ("punkt_name",)
    verbose_name = "Antwort"
    verbose_name_plural = "Checklisten-Antworten"


# --- Prüfung ---
@admin.register(Pruefung)
class PruefungAdmin(admin.ModelAdmin):
    list_display = ("geraet", "art", "datum", "pruefer", "bestanden", "naechste_pruefung")
    list_filter = ("art", "bestanden", "datum")
    search_fields = ("geraet__bezeichnung", "pruefer", "bemerkung")
    date_hierarchy = "datum"
    inlines = [AntwortInline]
    ordering = ("-datum",)

    fieldsets = (
        ("Allgemeine Daten", {
            "fields": ("geraet", "art", "datum", "pruefer", "bestanden", "bemerkung")
        }),
        ("Sonstiges", {
            "fields": ("feueron",),
            "classes": ("collapse",),
        }),
    )


# --- Antworten einzeln sichtbar (optional, aber hilfreich für Debug) ---
@admin.register(Antwort)
class AntwortAdmin(admin.ModelAdmin):
    list_display = ("pruefung", "punkt_name", "ok", "is_pflicht")
    list_filter = ("ok", "is_pflicht")
    search_fields = ("punkt_name", "bemerkung", "pruefung__geraet__bezeichnung")
    ordering = ("pruefung",)
