import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import IntegrityError
from geraete.models import Geraet, Geraetekategorie


class Command(BaseCommand):
    help = "Importiert Geräte aus einer CSV-Datei. Erstellt Kategorien automatisch, falls sie nicht existieren."

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Pfad zur CSV-Datei (Standard: BASE_DIR/import_geraete.csv)',
        )

    def handle(self, *args, **options):
        csv_path = options['file'] or os.path.join(settings.BASE_DIR, "import_geraete.csv")

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"❌ Datei nicht gefunden: {csv_path}"))
            return

        created_count = 0
        updated_count = 0
        duplicates = []

        self.stdout.write(self.style.NOTICE(f"📦 Import starte von: {csv_path}"))

        # 🧩 CSV robust öffnen
        try:
            with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                rows = list(reader)
        except UnicodeDecodeError:
            with open(csv_path, newline='', encoding='latin1') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                rows = list(reader)

        for row in rows:
            typ = row.get("Typ")
            identifikation = (row.get("Identifikation") or "").strip()
            barcode = (row.get("Barcode") or "").strip()

            if not identifikation:
                continue

            # Kategorie anlegen oder holen
            kategorie, _ = Geraetekategorie.objects.get_or_create(
                name=typ.strip() if typ else "Unbekannt"
            )

            # 🧠 Schritt 1: Prüfen, ob der Barcode schon vergeben ist
            if barcode:
                existing_barcode = Geraet.objects.filter(barcode=barcode).exclude(identifikation=identifikation)
                if existing_barcode.exists():
                    self.stdout.write(self.style.WARNING(
                        f"⚠️  Doppelter Barcode '{barcode}' gefunden "
                        f"(bereits bei {existing_barcode.first().identifikation}) – wird ignoriert." #type: ignore
                    ))
                    duplicates.append(barcode)
                    barcode = ""  # ⚠️ Barcode wird geleert

            # 🧠 Schritt 2: Gerät suchen oder anlegen (ohne UNIQUE-Konflikt)
            try:
                geraet, created = Geraet.objects.update_or_create(
                    identifikation=identifikation,
                    defaults={
                        "barcode": barcode or None,
                        "kategorie": kategorie,
                    },
                )
            except IntegrityError:
                # Fallback, falls es trotz allem kracht
                self.stdout.write(self.style.ERROR(
                    f"❌ UNIQUE-Fehler bei Identifikation '{identifikation}' mit Barcode '{barcode}' – wird übersprungen."
                ))
                continue

            if created:
                created_count += 1
            else:
                updated_count += 1

        # ✅ Zusammenfassung
        self.stdout.write(self.style.SUCCESS("✅ Import abgeschlossen."))
        self.stdout.write(self.style.SUCCESS(f"   ➕ {created_count} Geräte neu erstellt"))
        self.stdout.write(self.style.SUCCESS(f"   🔄 {updated_count} Geräte aktualisiert"))

        if duplicates:
            self.stdout.write(self.style.WARNING(
                f"🚨 Folgende Barcodes waren doppelt und wurden ignoriert: {', '.join(duplicates)}"
            ))
