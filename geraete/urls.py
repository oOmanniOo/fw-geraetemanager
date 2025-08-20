from django.urls import path
from . import views

urlpatterns = [
    path("", views.GeraetListView.as_view(), name="geraete_liste"),
    path("<int:pk>/", views.GeraetDetailView.as_view(), name="geraete_detail"),
    path("neu/", views.GeraetCreateView.as_view(), name="geraete_neu"),
    path("<int:pk>/bearbeiten/", views.GeraetUpdateView.as_view(), name="geraete_bearbeiten"),
    path("<int:pk>/loeschen/", views.GeraetDeleteView.as_view(), name="geraete_loeschen"),
]
