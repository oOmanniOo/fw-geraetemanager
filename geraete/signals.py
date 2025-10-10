from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Geraetekategorie, Status
    
@receiver(post_migrate)
def create_default_status(sender, **kwargs):
    if sender.name == 'geraete':
        for name in ['aktiv', 'defekt', 'ausgemustert']:
            Status.objects.get_or_create(name=name)
