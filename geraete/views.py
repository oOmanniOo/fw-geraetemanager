from django.db.models import Q
from django.core.paginator import Paginator 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from . models import Geraet, Geraetekategorie
from .forms import GeraetForm
from pruefungen.models import Pruefung

class GeraetListView(ListView):
    model = Geraet
    template_name = "geraete/geraet_liste.html"
    context_object_name = "geraete"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()

        # Suchparameter aus URL
        search_query = self.request.GET.get("q")
        kategorie_id = self.request.GET.get("kategorie")

        # Filter: Suche in barcode, bezeichnung, identifikation
        if search_query:
            queryset = queryset.filter(
                Q(barcode__icontains=search_query) |
                Q(bezeichnung__icontains=search_query) |
                Q(identifikation__icontains=search_query)
            )

        # Filter: Kategorie
        if kategorie_id and kategorie_id.isdigit():
            queryset = queryset.filter(kategorie_id=kategorie_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # alle Kategorien ins Template geben
        context["kategorien"] = Geraetekategorie.objects.all()
        return context
    
    
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
    form_class = GeraetForm
    success_url = reverse_lazy("geraete:liste")


class GeraetUpdateView(UpdateView):
    model = Geraet
    template_name = "geraete/geraet_form.html"
    form_class = GeraetForm
    success_url = reverse_lazy("geraete:liste")

class GeraetDeleteView(DeleteView):
    model = Geraet
    template_name = "geraete/geraet_bestaetigen_loeschen.html"
    success_url = reverse_lazy("geraete:liste")
