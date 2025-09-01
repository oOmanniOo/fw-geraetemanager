from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Geraeteraum

@receiver(post_migrate)
def create_default_geraeteraeume(sender, **kwargs):
    if sender.name == 'fahrzeuge':
        for name in ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'GR', 'Dach']:
            Geraeteraum.objects.get_or_create(bezeichnung=name)