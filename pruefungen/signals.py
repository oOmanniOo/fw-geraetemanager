from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Pruefungsart

@receiver(post_migrate)
def create_default_pruefungsart(sender, **kwargs):
    if sender.name == 'pruefung':
        for name in ['Prüfung nach Benutzung', 'Jährliche Prüfung', 'Prüfung vor Benutzung', ]:
            Pruefungsart.objects.get_or_create(name=name)