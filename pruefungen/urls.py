from django.urls import path
from . import views

app_name = 'pruefungen'

urlpatterns = [
     path('', views.pruefungs_uebersicht, name ='uebersicht'),
     path('start/<int:geraet_id>/', views.start_pruefung, name='start'),
     path('bearbeite/<int:pruefung_id>/', views.bearbeite_pruefung, name='bearbeite'),
     path('<int:pk>/', views.PruefungDetailView.as_view(), name='detail'),
     path('<int:pk>/pdf/', views.pruefung_pdf, name='pdf'),
     path('feueron/', views.FeueronListView.as_view(), name='feueron'),
     path('anstehende/', views.anstehende_pruefungen, name='anstehende'),
]