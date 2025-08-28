from django.contrib import admin
from django.urls import path, include
from geraete.views import GeraetListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GeraetListView.as_view(), name="geraete_liste"),
    path('geraete/', include('geraete.urls')),
    path('fahrzeuge/', include('fahrzeuge.urls')),
    path('pruefung/', include('pruefungen.urls')),
]
