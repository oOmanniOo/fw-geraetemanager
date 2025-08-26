from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import datetime
from .models import Pruefung, Pruefungsart, Checkliste, Checklistenpunkt, Antwort
from geraete.models import Geraet


def start_pruefung(request, geraet_id):
    geraet = get_object_or_404(Geraet, id=geraet_id)

    if request.method == 'POST':
        art_id = request.POST.get('art')
        art = get_object_or_404(Pruefungsart, id=art_id)
        checkliste = Checkliste.objects.filter(art=art, kategorie=geraet.kategorie).first()

        # Prüfung anlegen
        pruefung = Pruefung.objects.create(
            geraet=geraet,
            art=art,
            datum=timezone.now(),
            pruefer=request.user.username if request.user.is_authenticated else 'Unbekannt',
            bestanden=False  # wird später berechnet
        )

        # Antworten vorbereiten
        for punkt in checkliste.punkte.all():
            Antwort.objects.create(pruefung=pruefung, punkt=punkt, ok=False)

        return redirect('pruefungen:bearbeite_pruefung', pruefung_id=pruefung.id)

    arten = Pruefungsart.objects.all()
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
        
        # Checklistenpunkte verarbeiten
        bestanden = True
        for antwort in pruefung.antworten.all():
            ok = request.POST.get(f'punkt_{antwort.id}') == 'on'
            bemerkung = request.POST.get(f'bemerkung_{antwort.id}', '')
            antwort.ok = ok
            antwort.bemerkung = bemerkung
            antwort.save()
            if not ok and antwort.punkt.ist_pflicht:
                bestanden = False

        pruefung.bestanden = bestanden
        pruefung.save()
        return redirect('geraete:geraete_detail', pk=pruefung.geraet.id)  # zurück zum Gerät

    return render(request, 'pruefungen/bearbeite_pruefung.html', {'pruefung': pruefung})

def pruefungs_uebersicht(request):
    pruefungen = Pruefung.objects.all().order_by('-datum')

    geraet_filter = request.GET.get('geraet')
    art_filter = request.GET.get('art')
    bestanden_filter = request.GET.get('bestanden')

    if geraet_filter:
        pruefungen = pruefungen.filter(geraet_id=geraet_filter)

    if art_filter:
        pruefungen = pruefungen.filter(art_id=art_filter)
    
    if bestanden_filter in ['ja', 'nein']:
        pruefungen = pruefungen.filter(bestanden=bestanden_filter == 'ja')

    context = {
        'pruefungen': pruefungen, 
        'geraet_filter': geraet_filter,
        'art_filter': art_filter,
        'bestanden_filter': bestanden_filter,
    }

    return render(request, 'pruefungen/pruefungs_uebersicht.html', context)

