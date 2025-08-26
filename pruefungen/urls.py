from django.urls import path
from . import views

app_name = 'pruefungen'

urlpatterns = [
     path('', views.pruefungs_uebersicht, name ='pruefungs_uebersicht'),
     path('start/<int:geraet_id>/', views.start_pruefung, name='start_pruefung'),
     path('bearbeite/<int:pruefung_id>/', views.bearbeite_pruefung, name='bearbeite_pruefung'),
]