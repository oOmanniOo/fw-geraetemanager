from django.urls import path
from . import views

app_name = 'fahrzeuge'

urlpatterns = [
    path("", views.FahrzeugListView.as_view(), name="liste"),
    path("<int:pk>/", views.FahrzeugDetailView.as_view(), name="detail"),
    path("neu/", views.FahrzeugCreateView.as_view(), name="neu"),
    path("<int:pk>/bearbeiten/", views.FahrzeugUpdateView.as_view(), name="bearbeiten"),
    path("<int:pk>/loeschen/", views.FahrzeugDeleteView.as_view(), name="loeschen"),
]
