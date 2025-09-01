from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . models import Fahrzeug
from geraete.models import Geraet

class FahrzeugListView(ListView):
    model = Fahrzeug
    template_name = "fahrzeuge/fahrzeug_liste.html"
    context_object_name = "fahrzeuge"

class FahrzeugDetailView(DetailView):
    model = Fahrzeug
    template_name = "fahrzeuge/fahrzeug_detail.html"
    context_object_name = "fahrzeug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Geräte direkt über die related_name Beziehung laden
        geraete = self.object.geraete.all()
        context['geraete'] = geraete
        return context

class FahrzeugCreateView(CreateView):
    model = Fahrzeug
    template_name = "fahrzeuge/fahrzeug_form.html"
    fields = ["bezeichnung", "kennzeichen", "funkrufname", "standort", "aktiv"]
    success_url = reverse_lazy("fahrzeuge:liste")

class FahrzeugUpdateView(UpdateView):
    model = Fahrzeug
    template_name = "fahrzeuge/fahrzeug_form.html"
    fields = ["bezeichnung", "kennzeichen", "funkrufname", "standort", "aktiv"]
    success_url = reverse_lazy("fahrzeuge:liste")

class FahrzeugDeleteView(DeleteView):
    model = Fahrzeug
    template_name = "fahrzeuge/fahrzeug_bestaetigen_loeschen.html"
    success_url = reverse_lazy("fahrzeuge:liste")
