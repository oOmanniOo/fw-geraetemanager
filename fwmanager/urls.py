from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('geraete/', include('geraete.urls')),
    path('fahrzeuge/', include('fahrzeuge.urls')),
    path('pruefung/', include('pruefungen.urls')),
]
