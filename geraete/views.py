from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . models import Geraet
from pruefungen.models import Pruefung

class GeraetListView(ListView):
    model = Geraet
    template_name = "geraete/geraet_liste.html"
    context_object_name = "geraete"

class GeraetDetailView(DetailView):
    model = Geraet
    template_name = 'geraete/geraet_detail.html'
    context_object_name = 'geraet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pruefungen = Pruefung.objects.filter(geraet=self.object).order_by('-datum') #type: ignore

        paginator = Paginator(pruefungen, 5)  # 5 Prüfungen pro Seite
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['paginator'] = paginator
        context['pruefungen'] = page_obj.object_list
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        return context
        

class GeraetCreateView(CreateView):
    model = Geraet
    template_name = "geraete/geraet_form.html"
    fields = ["bezeichnung", "identifikation", "seriennummer", "kategorie", "status", "geraeteraum", "bemerkung"]
    success_url = reverse_lazy("geraete:liste")
class GeraetUpdateView(UpdateView):
    model = Geraet
    template_name = "geraete/geraet_form.html"
    fields = ["bezeichnung", "identifikation", "seriennummer", "kategorie", "status", "geraeteraum", "bemerkung"]
    success_url = reverse_lazy("geraete:liste")

class GeraetDeleteView(DeleteView):
    model = Geraet
    template_name = "geraete/geraet_bestaetigen_loeschen.html"
    success_url = reverse_lazy("geraete:liste")
