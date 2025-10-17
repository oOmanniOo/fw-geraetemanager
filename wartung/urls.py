from django.urls import path
from . import views

app_name = 'wartung'

urlpatterns = [
    path('', views.UebersichtListView.as_view(), name='uebersicht'),
    path('monat/', views.WartungListView.as_view(), name='wartungen_liste'),
]
 