from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect
from django.views.generic import ListView
from django.urls import reverse
from django.db.models import Q

from .models import Wartungszuordnung, Wartungsart, Wartungsvorgang

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar
# Create your views here.


class UebersichtListView(ListView):
    model = Wartungszuordnung
    template_name = 'wartung/wartung_uebersicht.html'
    context_object_name = 'wartungen'

    def get_queryset(self):
        # Nur aktive Zuordnungen, nach naechste_wartung sortiert
        return Wartungszuordnung.objects.filter(aktiv=True).order_by('naechste_wartung')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heute'] = date.today()
        return context
    

class WartungListView(ListView):  # Übersicht Monatswartung
    model = Wartungszuordnung
    template_name = 'wartung/wartung_monat.html'
    context_object_name = 'wartungen'

    def _monat_start_und_ende(self, basisdatum: date):
        start = basisdatum.replace(day=1)
        last_day = calendar.monthrange(basisdatum.year, basisdatum.month)[1]
        ende = basisdatum.replace(day=last_day)
        return start, ende

    def get_queryset(self):
        heute = date.today()
        start, ende = self._monat_start_und_ende(heute)

        qs = Wartungszuordnung.objects.filter(aktiv=True)

        fahrzeug_q = self.request.GET.get('fahrzeug')
        art_q = self.request.GET.get('art')
        geraet_q = self.request.GET.get('geraet')
        aktiv_q = self.request.GET.get('aktiv')

        if fahrzeug_q:
            qs = qs.filter(fahrzeug__bezeichnung__icontains=fahrzeug_q)
        if geraet_q:
            qs = qs.filter(geraet__identifikation__icontains=geraet_q)
        if art_q:
            qs = qs.filter(wartungsart__id=art_q)
        if aktiv_q in ("true", "false"):
            qs = qs.filter(aktiv=(aktiv_q == "true"))

        due_this_month = Q(naechste_wartung__gte=start, naechste_wartung__lte=ende)
        overdue = Q(naechste_wartung__lt=heute)
        no_next_date = Q(naechste_wartung__isnull=True)

        qs = qs.filter(due_this_month | overdue | no_next_date).order_by('naechste_wartung')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        heute = date.today()
        start, ende = self._monat_start_und_ende(heute)

        alle = self.get_queryset()
        context['heute'] = heute
        context['monat_start'] = start
        context['monat_ende'] = ende
        context['count_insgesamt'] = alle.count()
        context['count_ueberfaellig'] = alle.filter(naechste_wartung__lt=heute).count()
        context['arten'] = Wartungsart.objects.filter(aktiv=True).order_by('name')
        return context

    def post(self, request, *args, **kwargs):
        """
        Bulk-Aktionen per POST:
        Erwartet POST-Parameter:
          - action = 'complete_selected'
          - selected = list von wartungszuordnung-IDs
          - durchgefuehrt_von (optional)
          - bemerkung_<id> (optional pro Zeile)
        """
        action = request.POST.get('action')
        selected = request.POST.getlist('selected')

        if not action or not selected:
            return redirect(reverse('wartung:wartungen_liste'))

        durchgefuehrt_von = request.POST.get('durchgefuehrt_von', '').strip()

        if action == 'complete_selected':
            qs = Wartungszuordnung.objects.filter(pk__in=selected)

            for zu in qs:
                bemerkung = request.POST.get(f'bemerkung_{zu.id}', '').strip()  #type: ignore
                vorgang = Wartungsvorgang.objects.create(
                    zuordnung=zu,
                    status='abgeschlossen',
                    durchgefuehrt_von=durchgefuehrt_von or (
                        request.user.get_full_name() if request.user.is_authenticated else None
                    ),
                    bemerkung=bemerkung or 'Abgeschlossen via Monatsübersicht'
                )

                zu.letzte_wartung = vorgang.datum
                zu.naechste_wartung = zu.berechnung_naechste_wartung()
                zu.save()

            return redirect(reverse('wartung:wartungen_liste'))

        return redirect(reverse('wartung:wartungen_liste'))
