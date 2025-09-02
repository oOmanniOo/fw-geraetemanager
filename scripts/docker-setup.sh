#!/bin/bash

# Docker Setup Script für FW-Gerätemanager
echo "🚀 Starte Docker Setup für FW-Gerätemanager..."

# Prüfe ob Docker installiert ist
if ! command -v docker &> /dev/null; then
    echo "❌ Docker ist nicht installiert. Bitte installieren Sie Docker Desktop."
    exit 1
fi

# Prüfe ob Docker Compose installiert ist
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose ist nicht installiert."
    exit 1
fi

# Erstelle .env Datei falls nicht vorhanden
if [ ! -f .env ]; then
    echo "📝 Erstelle .env Datei..."
    cp env.example .env
    echo "✅ .env Datei erstellt"
fi

# Baue das Docker Image
echo "🔨 Baue Docker Image..."
docker-compose build

# Starte die Services
echo "🚀 Starte Services..."
docker-compose up -d

# Warte kurz bis der Service läuft
echo "⏳ Warte auf Service..."
sleep 10

# Führe Migrationen aus
echo "🗄️ Führe Datenbank-Migrationen aus..."
docker-compose exec web python manage.py migrate

# Erstelle Superuser falls gewünscht
read -p "🤔 Möchten Sie einen Superuser erstellen? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "👤 Erstelle Superuser..."
    docker-compose exec web python manage.py createsuperuser
fi

echo "✅ Setup abgeschlossen!"
echo "🌐 Die Anwendung ist verfügbar unter: http://localhost:8000"
echo "📊 Admin-Interface: http://localhost:8000/admin"
echo ""
echo "🔧 Nützliche Befehle:"
echo "  - Services stoppen: docker-compose down"
echo "  - Logs anzeigen: docker-compose logs -f"
echo "  - Shell öffnen: docker-compose exec web python manage.py shell"

