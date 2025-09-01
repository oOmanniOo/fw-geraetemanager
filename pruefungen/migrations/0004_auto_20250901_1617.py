from django.db import migrations

def create_pruefungsarten(apps, schema_editor):
    Pruefungsart = apps.get_model('pruefungen', 'Pruefungsart')

    pruefungsarten = [
        'Sichtprüfung',
        'Jährliche Prüfung',
        'Prüfung nach Benutzung'
    ]
    
    for name in pruefungsarten:
        Pruefungsart.objects.get_or_create(name=name)

def reverse_pruefungsarten(apps, schema_editor):
    Pruefungsart = apps.get_model('pruefungen', 'Pruefungsart')
    # Alle erstellten Prüfungsarten wieder löschen
    Pruefungsart.objects.filter(
        name__in=[
            'Sichtprüfung', 'Jährliche Prüfung', 'Prüfung nach Benutzung'
        ]
    ).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('pruefungen', '0001_initial'),  # Abhängigkeit von der Model-Migration
    ]

    operations = [
        migrations.RunPython(create_pruefungsarten, reverse_pruefungsarten),
    ]