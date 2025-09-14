from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView
from django.utils import timezone
from datetime import date, datetime
from .models import Pruefung, Pruefungsart, Checkliste, Antwort
from geraete.models import Geraet

from weasyprint import HTML

def anstehende_pruefungen(request):
    naechste_pruefungen_dict = {}
    today = date.today()

    # Filter queryset based on GET parameters
    geraet_filter = request.GET.get('geraet')
    art_filter = request.GET.get('art')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    alle_pruefungen = Pruefung.objects.select_related('geraet', 'art').order_by('datum')

    if geraet_filter:
        alle_pruefungen = alle_pruefungen.filter(geraet__bezeichnung__icontains=geraet_filter)
    
    if art_filter:
        alle_pruefungen = alle_pruefungen.filter(art_id=art_filter)

    for pruefung in alle_pruefungen:
        naechste = pruefung.naechste_pruefung
        if naechste:
            key = (pruefung.geraet.id, pruefung.art.id)
            naechste_pruefungen_dict[key] = {
                'geraet_name': pruefung.geraet.bezeichnung,
                'geraet_id': pruefung.geraet.id,
                'art_name': pruefung.art.name,
                'letzte_pruefung_datum': pruefung.datum,
                'naechste_pruefung_datum': naechste,
            }

    anstehende_liste = [p for p in naechste_pruefungen_dict.values() if p['naechste_pruefung_datum'] >= today]

    # Date range filtering
    start_date = None
    if start_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            anstehende_liste = [p for p in anstehende_liste if p['naechste_pruefung_datum'] >= start_date]
        except ValueError:
            pass # Ignore invalid date format

    end_date = None
    if end_date_str:
        try:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            anstehende_liste = [p for p in anstehende_liste if p['naechste_pruefung_datum'] <= end_date]
        except ValueError:
            pass # Ignore invalid date format

    anstehende_liste.sort(key=lambda p: p['naechste_pruefung_datum'])

    arten = Pruefungsart.objects.all()

    context = {
        'anstehende_pruefungen': anstehende_liste,
        'arten': arten,
        'geraet_filter': geraet_filter,
        'art_filter': art_filter,
        'start_date': start_date_str,
        'end_date': end_date_str,
    }

    return render(request, 'pruefungen/anstehende_pruefungen.html', context)

def start_pruefung(request, geraet_id):
    geraet = get_object_or_404(Geraet, id=geraet_id)

    if request.method == 'POST':
        art_id = request.POST.get('art')
        art = get_object_or_404(Pruefungsart, id=art_id)
        checkliste = Checkliste.objects.filter(art=art, kategorie=geraet.kategorie).first()

        # Prüfung anlegen (Datum als date, nicht datetime)
        pruefung = Pruefung.objects.create(
            geraet=geraet,
            art=art,
            datum=timezone.now().date(),
            pruefer=request.user.username if request.user.is_authenticated else 'Unbekannt',
            bestanden=None  # wird später berechnet
        )

        # Antworten vorbereiten: punkt_name und is_pflicht übernehmen
        if checkliste:
            for punkt in checkliste.punkte.all():   # type: ignore
                Antwort.objects.create(
                    pruefung=pruefung,
                    punkt=punkt,
                    punkt_name=punkt.name,
                    is_pflicht=punkt.ist_pflicht,
                    ok=False
                )

        return redirect('pruefungen:bearbeite', pruefung_id=pruefung.id)   # type: ignore

    arten = Pruefungsart.objects.filter(geraetekategorie=geraet.kategorie)
    return render(request, 'pruefungen/start_pruefung.html', {'geraet': geraet, 'arten': arten})


def bearbeite_pruefung(request, pruefung_id):
    pruefung = get_object_or_404(Pruefung, id=pruefung_id)

    if request.method == 'POST':
        # Prüfungsdetails aktualisieren
        pruefungsdatum = request.POST.get('pruefungsdatum')
        if pruefungsdatum:
            try:
                pruefung.datum = datetime.strptime(pruefungsdatum, '%Y-%m-%d').date()
            except ValueError:
                pass  # Bei ungültigem Datum wird das ursprüngliche beibehalten
        
        pruefer = request.POST.get('pruefer')
        if pruefer:
            pruefung.pruefer = pruefer
        
        allgemeine_bemerkung = request.POST.get('allgemeine_bemerkung')
        if allgemeine_bemerkung is not None:
            pruefung.bemerkung = allgemeine_bemerkung

        # Checkbox aus POST: existenz prüfen
        pruefung.feueron = request.POST.get('feueron') == 'on'
        
        # Checklistenpunkte verarbeiten
        antworten = pruefung.antworten.all()  # type: ignore
        if antworten.exists():
            bestanden = True
            for antwort in antworten:   # type: ignore
                ok = request.POST.get(f'punkt_{antwort.id}') == 'on'
                bemerkung = request.POST.get(f'bemerkung_{antwort.id}', '')
                antwort.ok = ok
                antwort.bemerkung = bemerkung
                # sicherstellen, dass punkt_name/is_pflicht erhalten bleiben bzw. aktualisiert werden
                if antwort.punkt:
                    antwort.punkt_name = antwort.punkt.name
                    antwort.is_pflicht = antwort.punkt.ist_pflicht
                antwort.save()
                # Pflicht prüfen: falls punkt gelöscht -> fallback auf gespeichertes is_pflicht
                pflicht = (antwort.punkt.ist_pflicht if antwort.punkt else antwort.is_pflicht)
                if not ok and pflicht:
                    bestanden = False
            pruefung.bestanden = bestanden
        else:
            # keine Checkliste -> manueller Status
            pruefung.bestanden = request.POST.get('manuell_bestanden') == 'on'
        
        pruefung.save()
        

        return redirect("geraete:detail", pk=pruefung.geraet.id)   # type: ignore

    return render(request, 'pruefungen/bearbeite_pruefung.html', {'pruefung': pruefung})

def pruefungs_uebersicht(request):
    pruefungen = Pruefung.objects.all().order_by('-datum')
    arten = Pruefungsart.objects.all()

    geraet_filter = request.GET.get('geraet')
    art_filter = request.GET.get('art')
    bestanden_filter = request.GET.get('bestanden')

    if geraet_filter:
        pruefungen = pruefungen.filter(geraet__bezeichnung__icontains=geraet_filter)

    if art_filter:
        pruefungen = pruefungen.filter(art_id=art_filter)
    
    if bestanden_filter:
        if bestanden_filter.lower() in ['true']:
            pruefungen = pruefungen.filter(bestanden=True)
        elif bestanden_filter.lower() in ['false']:
            pruefungen = pruefungen.filter(bestanden=False)

    paginator = Paginator(pruefungen, 20)  
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    context = {
        'arten': arten,
        'pruefungen': page,  # page ist das aktuelle Page-Objekt
        'page_obj': page,    # für das Pagination-Template
        'paginator': paginator,
        'is_paginated': page.has_other_pages(),
        'geraet_filter': geraet_filter,
        'art_filter': art_filter,
        'bestanden_filter': bestanden_filter,
    }
    return render(request, 'pruefungen/pruefungs_uebersicht.html', context)

class PruefungDetailView(DetailView):
    model = Pruefung
    template = 'pruefungen/pruefung_detail.html'
    context_object_name = 'pruefung'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Statt __debug_context nehmen wir einen erlaubten Key
        context["debug_context"] = context
        return context


def pruefung_pdf(request, pk):
    pruefung = get_object_or_404(Pruefung, pk=pk)

    html_string = render_to_string("pruefungen/pruefung_pdf.html", {"object": pruefung})

    # PDF erzeugen
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{pruefung.geraet.bezeichnung}_{pruefung.geraet.barcode}_{pruefung.art.name}_{pruefung.datum}.pdf"'  # type: ignore
    return response

class FeueronListView(ListView):
    model = Pruefung
    template_name = 'pruefungen/pruefung_feueron_liste.html'
    context_object_name = 'pruefungen'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Alle Prüfungsarten für das Dropdown-Menü
        context['arten'] = Pruefungsart.objects.all().order_by('name')
        
        # Aktuelle Filter-Werte für die Form
        context['current_geraet_filter'] = self.request.GET.get('geraet', '')
        context['current_art_filter'] = self.request.GET.get('art', '')
        context['current_bestanden_filter'] = self.request.GET.get('bestanden', '')
        
        # Optional: Die aktuell ausgewählte Prüfungsart als Objekt
        art_filter = self.request.GET.get('art')
        if art_filter:
            try:
                context['selected_pruefungsart'] = Pruefungsart.objects.get(id=art_filter)
            except Pruefungsart.DoesNotExist:
                context['selected_pruefungsart'] = None
        else:
            context['selected_pruefungsart'] = None
            
        return context

    def get_queryset(self):
        geraet_filter = self.request.GET.get('geraet')
        art_filter = self.request.GET.get('art')
        bestanden_filter = self.request.GET.get('bestanden')

        queryset = Pruefung.objects.filter(feueron=False)

        if geraet_filter:
            queryset = queryset.filter(geraet__bezeichnung__icontains=geraet_filter)

        if art_filter:
            queryset = queryset.filter(art_id=art_filter)

        if bestanden_filter:
            if bestanden_filter.lower() in ['true']:
                queryset = queryset.filter(bestanden=True)
            elif bestanden_filter.lower() in ['false']:
                queryset = queryset.filter(bestanden=False)

        return queryset.order_by('-datum')