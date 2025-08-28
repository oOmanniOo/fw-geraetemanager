from django.urls import path
from . import views

app_name = 'geraete'

urlpatterns = [
    path("", views.GeraetListView.as_view(), name="liste"),
    path("<int:pk>/", views.GeraetDetailView.as_view(), name="detail"),
    path("neu/", views.GeraetCreateView.as_view(), name="neu"),
    path("<int:pk>/bearbeiten/", views.GeraetUpdateView.as_view(), name="bearbeiten"),
    path("<int:pk>/loeschen/", views.GeraetDeleteView.as_view(), name="loeschen"),
]
