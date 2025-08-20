from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . models import Geraet

class GeraetListView(ListView):
    model = Geraet
    template_name = "geraete/geraet_liste.html"
    context_object_name = "geraete"

class GeraetDetailView(DetailView):
    model = Geraet
    template_name = "geraete/geraet_detail.html"

class GeraetCreateView(CreateView):
    model = Geraet
    template_name = "geraete/geraet_form.html"
    fields = ["bezeichnung", "identifikation", "seriennummer", "kategorie", "status", "fahrzeug", "bemerkung"]
    success_url = reverse_lazy("geraete_liste")

class GeraetUpdateView(UpdateView):
    model = Geraet
    template_name = "geraete/geraet_form.html"
    fields = ["bezeichnung", "identifikation", "seriennummer", "kategorie", "status", "fahrzeug", "bemerkung"]
    success_url = reverse_lazy("geraete_liste")

class GeraetDeleteView(DeleteView):
    model = Geraet
    template_name = "geraete/geraet_bestaetigen_loeschen.html"
    success_url = reverse_lazy("geraete_liste")
