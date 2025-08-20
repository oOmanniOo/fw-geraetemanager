from django.contrib import admin
from .models import Pruefungsart, Checkliste, Checklistenpunkt, Pruefung, Antwort

# Register your models here.

admin.site.register(Pruefungsart)
admin.site.register(Checkliste)
admin.site.register(Checklistenpunkt)
admin.site.register(Pruefung)
admin.site.register(Antwort)
